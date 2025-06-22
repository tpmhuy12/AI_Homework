import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
ProductDemand = ctrl.Antecedent(np.arange(0, 11, 0.5), 'ProductDemand')
ComPriPress = ctrl.Antecedent(np.arange(0, 11, 0.5), 'ComPriPress')
StoRepu = ctrl.Antecedent(np.arange(0, 5.1, 0.1), 'StoRepu')
ProfitMargin = ctrl.Antecedent(np.arange(0, 11, 0.5), 'ProfitMargin')
SeasonDemand = ctrl.Antecedent(np.arange(0, 11, 0.5), 'SeasonDemand')

DiscountRate = ctrl.Consequent(np.arange(0, 71, 1), 'DiscountRate')

# Hàm thành viên cho ProductDemand (Nhu cầu sản phẩm)
ProductDemand["L"] = fuzz.trimf(ProductDemand.universe, [0, 0, 5])      # Thấp
ProductDemand["M"] = fuzz.trimf(ProductDemand.universe, [2.5, 5, 7.5])  # Trung bình
ProductDemand["H"] = fuzz.trimf(ProductDemand.universe, [5, 10, 10])    # Cao

# Hàm thành viên cho ComPriPress (Áp lực định giá của đối thủ cạnh tranh)
ComPriPress["L"] = fuzz.trimf(ComPriPress.universe, [0, 0, 5])          # Thấp
ComPriPress["M"] = fuzz.trimf(ComPriPress.universe, [2.5, 5, 7.5])      # Trung bình
ComPriPress["H"] = fuzz.trimf(ComPriPress.universe, [5, 10, 10])        # Cao

# Hàm thành viên cho StoRepu (Uy tín cửa hàng)
StoRepu["L"] = fuzz.trimf(StoRepu.universe, [0, 0, 4])                  # Thấp (dưới 4 sao)
StoRepu["M"] = fuzz.trimf(StoRepu.universe, [3.8, 4.2, 4.5])            # Trung bình (4.0 - 4.5 sao)
StoRepu["H"] = fuzz.trimf(StoRepu.universe, [4.3, 5, 5])                # Cao (trên 4.5 sao)

# Hàm thành viên cho ProfitMargin (Biên lợi nhuận)
ProfitMargin["L"] = fuzz.trimf(ProfitMargin.universe, [0, 0, 4])        # Thấp
ProfitMargin["M"] = fuzz.trimf(ProfitMargin.universe, [3, 5, 7])        # Trung bình
ProfitMargin["H"] = fuzz.trimf(ProfitMargin.universe, [6, 10, 10])      # Cao

# Hàm thành viên cho SeasonDemand (Nhu cầu theo mùa)
SeasonDemand["L"] = fuzz.trimf(SeasonDemand.universe, [0, 0, 4])        # Không có
SeasonDemand["M"] = fuzz.trimf(SeasonDemand.universe, [3, 5, 7])        # Trung bình
SeasonDemand["H"] = fuzz.trimf(SeasonDemand.universe, [6, 10, 10])      # Cao

# Hàm thành viên cho DiscountRate (Tỷ lệ phần trăm chiết khấu)
DiscountRate["VL"] = fuzz.trimf(DiscountRate.universe, [0, 0, 5])       # Rất thấp (0-5%)
DiscountRate["L"]  = fuzz.trimf(DiscountRate.universe, [3, 7, 10])      # Thấp (5-10%)
DiscountRate["M"]  = fuzz.trimf(DiscountRate.universe, [8, 15, 25])     # Trung bình (10-20%)
DiscountRate["H"]  = fuzz.trimf(DiscountRate.universe, [20, 30, 40])    # Cao (20-40%)
DiscountRate["VH"] = fuzz.trimf(DiscountRate.universe, [35, 50, 70])    # Rất cao (40-70%)


# Các luật shopee
# 1. Nếu (Nhu cầu sản phẩm cao) VÀ (Áp lực định giá của đối thủ cạnh tranh thấp) VÀ (Biên lợi nhuận thấp) Thì Giảm giá rất thấp.
rule1 = ctrl.Rule(ProductDemand["H"] & ComPriPress["L"] & ProfitMargin["L"], DiscountRate["VL"])

# 2. Nếu (Nhu cầu sản phẩm thấp) VÀ (Áp lực định giá của đối thủ cạnh tranh cao) VÀ (Biên lợi nhuận cao) Thì Chiết khấu cao.
rule2 = ctrl.Rule(ProductDemand["L"] & ComPriPress["H"] & ProfitMargin["H"], DiscountRate["H"])

# 3. Nếu (Uy tín cửa hàng cao) VÀ (Biên lợi nhuận trung bình) VÀ (Nhu cầu theo mùa cao) Thì Chiết khấu trung bình.
rule3 = ctrl.Rule(StoRepu["H"] & ProfitMargin["M"] & SeasonDemand["H"], DiscountRate["M"])

# 4. Nếu (Áp lực định giá của đối thủ cạnh tranh cao) VÀ (Nhu cầu theo mùa cao) VÀ (Biên lợi nhuận cao) Thì Chiết khấu rất cao.
rule4 = ctrl.Rule(ComPriPress["H"] & SeasonDemand["H"] & ProfitMargin["H"], DiscountRate["VH"])

# 5. Nếu (Uy tín cửa hàng thấp) VÀ (Nhu cầu sản phẩm trung bình) VÀ (Biên lợi nhuận thấp) Thì Chiết khấu trung bình.
rule5 = ctrl.Rule(StoRepu["L"] & ProductDemand["M"] & ProfitMargin["L"], DiscountRate["M"])

# 6. Nếu (Nhu cầu sản phẩm cao) VÀ (Nhu cầu theo mùa không có) VÀ (Áp lực định giá của đối thủ cạnh tranh thấp) Thì Chiết khấu rất thấp.
rule6 = ctrl.Rule(ProductDemand["H"] & SeasonDemand["L"] & ComPriPress["L"], DiscountRate["VL"])

# 7. Nếu (Biên lợi nhuận cao) VÀ (Áp lực định giá của đối thủ cạnh tranh là Trung bình) VÀ (Cầu theo mùa là Trung bình) Thì Chiết khấu là Trung bình.
rule7 = ctrl.Rule(ProfitMargin["H"] & ComPriPress["M"] & SeasonDemand["M"], DiscountRate["M"])

# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7
])

shopee_system = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ
shopee_system.input['ProductDemand'] =  9   # Nhu cầu sản phẩm cao (giá trị thuộc "H")
shopee_system.input['ComPriPress'] =  6   # Áp lực định giá của đối thủ cạnh tranh trung bình (giá trị thuộc "M")
shopee_system.input['ProfitMargin'] = 9      # Biên lợi nhuận cao (giá trị thuộc "H")
shopee_system.input['StoRepu'] = 4.2   # Sự kiện mùa cao (giá trị thuộc "H")
shopee_system.input['SeasonDemand'] = 7       # Nhu cầu theo mùa cao (giá trị thuộc "H")

# Tính toán
shopee_system.compute()

# Xuất kết quả
print("Tỷ lệ phần trăm chiết khấu: ", shopee_system.output['DiscountRate'])



# Hiển thị đồ thị kết quả
ProductDemand.view()
ComPriPress.view()
ProfitMargin.view() 
StoRepu.view()
SeasonDemand.view()
DiscountRate.view(sim=shopee_system)

plt.show()