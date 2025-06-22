import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
StoreRate = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'StoreRate')
SaleVolume = ctrl.Antecedent(np.arange(0, 101, 1), 'SaleVolume')
ProfitMargin = ctrl.Antecedent(np.arange(0, 101, 1), 'ProfitMargin')
SeasonEvent = ctrl.Antecedent(np.arange(0, 6, 1), 'SeasonEvent')
CompeDis = ctrl.Antecedent(np.arange(0, 101, 1), 'CompeDis')

DiscountRate = ctrl.Consequent(np.arange(0, 71, 1), 'DiscountRate')

# Hàm thành viên cho StoreRate   # Khoảng cách
StoreRate["L"] =    fuzz.trimf(StoreRate.universe, [0, 0, 4]) # Đánh giá thấp
StoreRate["M"] =    fuzz.trimf(StoreRate.universe, [4, 4, 5])  # Đánh giá trung bình
StoreRate["H"] =    fuzz.trimf(StoreRate.universe, [4.5, 5, 5])  # Đánh giá cao


# Hàm thành viên cho SaleVolume     
SaleVolume["L"] = fuzz.trimf(SaleVolume.universe, [0, 0, 30]) # Giao thông thấp
SaleVolume["M"] = fuzz.trimf(SaleVolume.universe, [20, 45, 70]) # Giao thông trung bình
SaleVolume["H"] = fuzz.trimf(SaleVolume.universe, [60, 80, 100])    # Giao thông cao


# Hàm thành viên cho ProfitMargin   #biên lợi nhuận
ProfitMargin["L"] = fuzz.trimf(ProfitMargin.universe, [0, 0, 30])   # Nhu cầu thấp
ProfitMargin["M"] = fuzz.trimf(ProfitMargin.universe, [20, 45, 70])     # Nhu cầu trung bình
ProfitMargin["H"] = fuzz.trimf(ProfitMargin.universe, [60, 80, 100])   # Nhu cầu cao

# Hàm thành viên cho SeasonEvent/ Sự kiện mùa
SeasonEvent["L"] = fuzz.trimf(SeasonEvent.universe, [0, 0, 3])     # Thấp
SeasonEvent["M"] = fuzz.trimf(SeasonEvent.universe, [2, 3, 4])     # Trung Bình
SeasonEvent["H"] = fuzz.trimf(SeasonEvent.universe, [3, 4, 5])     # Cao


# Hàm thành viên cho CompeDis / Giảm giá đối thủ cạnh tranh
CompeDis["L"] = fuzz.trimf(CompeDis.universe, [0, 0, 50])   # Thấp
CompeDis["M"] = fuzz.trimf(CompeDis.universe, [40, 60, 80]) # Trung Bình
CompeDis["H"] = fuzz.trimf(CompeDis.universe, [70, 85, 100])# Cao

# Hàm thành viên cho DiscountRate  # Tỷ lệ phần trăm chiết khấu
DiscountRate["VL"] = fuzz.trimf(DiscountRate.universe, [0, 0, 5])  # Không có chiết khấu
DiscountRate["L"] = fuzz.trimf(DiscountRate.universe, [5, 5, 10])  # Giá thấp
DiscountRate["M"] = fuzz.trimf(DiscountRate.universe, [10, 15, 20])  # Giá trung bình
DiscountRate["H"] = fuzz.trimf(DiscountRate.universe, [20, 30, 40]) # Giá cao
DiscountRate["VH"] = fuzz.trimf(DiscountRate.universe, [40, 55, 70])    # Giá rất cao



# Các luật shopee
# 1. Nếu (Xếp hạng cửa hàng cao) VÀ (Khối lượng bán hàng cao) VÀ (Biên lợi nhuận cao) Thì Chiết khấu rất thấp.
rule1 = ctrl.Rule(StoreRate["H"] & SaleVolume["H"] & ProfitMargin["H"], DiscountRate["VL"])

# 2. Nếu (Xếp hạng cửa hàng thấp) VÀ (Khối lượng bán hàng thấp) VÀ (Biên lợi nhuận cao) Thì Chiết khấu cao.
rule2 = ctrl.Rule(StoreRate["L"] & SaleVolume["L"] & ProfitMargin["H"], DiscountRate["H"])

# 3. Nếu (Sự kiện theo mùa cao) VÀ (Chiết khấu của đối thủ cao) Thì Chiết khấu rất cao.
rule3 = ctrl.Rule(SeasonEvent["H"] & CompeDis["H"], DiscountRate["VH"])

# 4. Nếu (Xếp hạng cửa hàng là Trung bình) VÀ (Khối lượng bán hàng là Trung bình) VÀ (Biên lợi nhuận là Trung bình) Thì Chiết khấu là Trung bình.
rule4 = ctrl.Rule(StoreRate["M"] & SaleVolume["M"] & ProfitMargin["M"], DiscountRate["M"])

# 5. Nếu (Chiết khấu của đối thủ cạnh tranh là Thấp) VÀ (Biên lợi nhuận là Thấp) VÀ (Khối lượng bán hàng là Cao) Thì Chiết khấu là Rất thấp.
rule5 = ctrl.Rule(CompeDis["L"] & ProfitMargin["L"] & SaleVolume["H"], DiscountRate["VL"])

# 6. Nếu (Xếp hạng cửa hàng là Thấp) VÀ (Sự kiện theo mùa là Không có) Thì Chiết khấu là Trung bình.
rule6 = ctrl.Rule(StoreRate["L"] & SeasonEvent["L"], DiscountRate["M"])

# 7. Nếu (Khối lượng bán hàng là Thấp) VÀ (Biên lợi nhuận là Thấp) Thì Chiết khấu là Rất cao.
rule7 = ctrl.Rule(SaleVolume["L"] & ProfitMargin["L"], DiscountRate["VH"])

# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6,
    rule7
])

shopee_system = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ
shopee_system.input['StoreRate'] =  4.3   # Khoảng cách dài (giá trị thuộc "L")
shopee_system.input['SaleVolume'] = 50     # Giao thông trung bình (giá trị thuộc "M")
shopee_system.input['ProfitMargin'] = 14       # Nhu cầu thấp (giá trị thuộc "L")
shopee_system.input['SeasonEvent'] = 4.5   # Sự kiện mùa cao (giá trị thuộc "H")
shopee_system.input['CompeDis'] = 85        # Giảm giá đối thủ cao (giá trị thuộc "H")

# Tính toán
shopee_system.compute()

# Xuất kết quả
print("Tỷ lệ phần trăm chiết khấu: ", shopee_system.output['DiscountRate'])



# Hiển thị đồ thị kết quả
StoreRate.view()
SaleVolume.view()
ProfitMargin.view() 
SeasonEvent.view()
CompeDis.view()
DiscountRate.view(sim=shopee_system)

plt.show()