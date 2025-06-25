import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
RideDistance = ctrl.Antecedent(np.arange(0, 51, 1), 'RideDistance')
TrafficCon = ctrl.Antecedent(np.arange(0, 101, 1), 'TrafficCon')
DemandLv = ctrl.Antecedent(np.arange(0, 101, 1), 'DemandLv')
WeatherCon = ctrl.Antecedent(np.arange(0, 6, 0.5), 'WeatherCon')
CusRate = ctrl.Antecedent(np.arange(1, 5.5, 0.5), 'CusRate')
RidePunc = ctrl.Antecedent(np.arange(0, 101, 1), 'RidePunc')

Price = ctrl.Consequent(np.arange(0, 11, 1), 'Price')
RePoint = ctrl.Consequent(np.arange(0, 11, 1), 'RePoint')

# Hàm thành viên cho RideDistance   # Khoảng cách
RideDistance["S"] = fuzz.trimf(RideDistance.universe, [0, 0, 3])   # Khoảng cách ngắn
RideDistance["M"] = fuzz.trimf(RideDistance.universe, [2, 5, 8])  # Khoảng cách trung bình
RideDistance["L"] = fuzz.trimf(RideDistance.universe, [6, 13, 20])  # Khoảng cách dài
RideDistance["VL"] = fuzz.trimf(RideDistance.universe, [15, 33, 50])  # Khoảng cách rất dài/xa

# Hàm thành viên cho TrafficCon     
TrafficCon["L"] = fuzz.trimf(TrafficCon.universe, [0, 0, 30]) # Giao thông thấp
TrafficCon["M"] = fuzz.trimf(TrafficCon.universe, [20, 45, 70]) # Giao thông trung bình
TrafficCon["H"] = fuzz.trimf(TrafficCon.universe, [60, 80, 100])    # Giao thông cao


# Hàm thành viên cho DemandLv   # Nhu cầu
DemandLv["L"] = fuzz.trimf(DemandLv.universe, [0, 0, 30])   # Nhu cầu thấp
DemandLv["M"] = fuzz.trimf(DemandLv.universe, [20, 45, 70])     # Nhu cầu trung bình
DemandLv["H"] = fuzz.trimf(DemandLv.universe, [60, 80, 100])   # Nhu cầu cao

# Hàm thành viên cho WeatherCon/ Điều kiện thời tiết
WeatherCon["B"] = fuzz.trimf(WeatherCon.universe, [0, 0, 2])     # bad
WeatherCon["M"] = fuzz.trimf(WeatherCon.universe, [1.5, 3, 4])     # Moderate
WeatherCon["G"] = fuzz.trimf(WeatherCon.universe, [3, 4, 5])     # Good

# Hàm thành viên cho CusRate / Đánh giá khách hàng
CusRate["P"] = fuzz.trimf(CusRate.universe, [1, 1, 2.5])    # Đánh giá kém
CusRate["A"] = fuzz.trimf(CusRate.universe, [2, 3, 4])   # Đánh giá trung bình
CusRate["G"] = fuzz.trimf(CusRate.universe, [3.5, 5, 5])    # Đánh giá tốt

# Hàm thành viên cho RidePunc / Đúng giờ
RidePunc["L"] = fuzz.trimf(RidePunc.universe, [0, 0, 50])   # Trễ
RidePunc["O"] = fuzz.trimf(RidePunc.universe, [40, 60, 80]) # Đúng giờ
RidePunc["E"] = fuzz.trimf(RidePunc.universe, [70, 85, 100])# Sớm

# Hàm thành viên cho Price  # Giá
Price["L"] = fuzz.trimf(Price.universe, [0, 0, 4])  # Giá thấp
Price["M"] = fuzz.trimf(Price.universe, [3, 5, 7])  # Giá trung bình
Price["H"] = fuzz.trimf(Price.universe, [5, 7, 9]) # Giá cao
Price["VH"] = fuzz.trimf(Price.universe, [8, 10, 10])    # Giá rất cao

# Hàm thành viên cho RePoint    # Điểm thưởng
RePoint["N"] = fuzz.trimf(RePoint.universe, [0, 0, 4])  # Không có điểm thưởng
RePoint["F"] = fuzz.trimf(RePoint.universe, [3, 5, 7])  # Điểm thưởng ít
RePoint["M"] = fuzz.trimf(RePoint.universe, [5, 7, 9])  # Điểm thưởng trung bình
RePoint["H"] = fuzz.trimf(RePoint.universe, [7, 9, 10])  # Điểm thưởng cao


# Các luật grab
# 1. Nếu (Khoảng cách ngắn) VÀ (Giao thông thấp) VÀ (Nhu cầu thấp), THÌ Giá thấp.
rule1 = ctrl.Rule(RideDistance["S"] & TrafficCon["L"] & DemandLv["L"], Price["L"])

# 2. Nếu (Khoảng cách ngắn) VÀ (Giao thông trung bình) VÀ (Nhu cầu cao), THÌ Giá trung bình.
rule2 = ctrl.Rule(RideDistance["S"] & TrafficCon["M"] & DemandLv["H"], Price["M"])

# 3. Nếu (Khoảng cách trung bình) VÀ (Giao thông cao) VÀ (Nhu cầu cao), THÌ Giá cao.
rule3 = ctrl.Rule(RideDistance["M"] & TrafficCon["H"] & DemandLv["H"], Price["H"])

# 4. Nếu (Khoảng cách dài) VÀ (Giao thông trung bình) VÀ (Thời tiết tốt), THÌ Giá trung bình.
rule4 = ctrl.Rule(RideDistance["L"] & TrafficCon["M"] & WeatherCon["G"], Price["M"])

# 5. Nếu (Khoảng cách dài) VÀ (Giao thông cao) VÀ (Thời tiết xấu), THÌ Giá cao.
rule5 = ctrl.Rule(RideDistance["L"] & TrafficCon["H"] & WeatherCon["B"], Price["H"])

# 6. Nếu (Khoảng cách rất xa) VÀ (Giao thông cao) VÀ (Nhu cầu cao), THÌ Giá cao.
rule6 = ctrl.Rule(RideDistance["VL"] & TrafficCon["H"] & DemandLv["H"], Price["H"])

# 7. Nếu (Khoảng cách trung bình) VÀ (Giao thông thấp) VÀ (Nhu cầu thấp), THÌ Giá trung bình.
rule7 = ctrl.Rule(RideDistance["M"] & TrafficCon["L"] & DemandLv["L"], Price["M"])

# 8. Nếu (Khoảng cách ngắn) VÀ (Lưu lượng giao thông cao) VÀ (Thời tiết xấu), THÌ Giá cao.
rule8 = ctrl.Rule(RideDistance["S"] & TrafficCon["H"] & WeatherCon["B"], Price["H"])

# 9. Nếu (Khoảng cách rất xa) VÀ (Thời tiết xấu), THÌ Giá rất cao.
rule9 = ctrl.Rule(RideDistance["VL"] & WeatherCon["B"], Price["H"])

# 10. Nếu (Khoảng cách trung bình) VÀ (Lưu lượng giao thông trung bình) VÀ (Thời tiết vừa phải), THÌ Giá trung bình.
rule10 = ctrl.Rule(RideDistance["M"] & TrafficCon["M"] & WeatherCon["M"], Price["M"])

# 11. Nếu (Đánh giá của khách hàng tốt) VÀ (Đúng giờ sớm), THÌ Điểm thưởng cao.
rule11 = ctrl.Rule(CusRate["G"] & RidePunc["E"], RePoint["H"])

# 12. Nếu (Đánh giá của khách hàng trung bình) VÀ (Đúng giờ đúng giờ), THÌ Điểm thưởng trung bình.
rule12 = ctrl.Rule(CusRate["A"] & RidePunc["O"], RePoint["M"])

# 13. Nếu (Đánh giá của khách hàng kém) VÀ (Đúng giờ muộn), THÌ Điểm thưởng không có.
rule13 = ctrl.Rule(CusRate["P"] & RidePunc["L"], RePoint["N"])

# 14. Nếu (Khoảng cách dài) VÀ (Lưu lượng giao thông cao) VÀ (Đi xe đúng giờ đúng giờ), THÌ Điểm thưởng cao.
rule14 = ctrl.Rule(RideDistance["L"] & TrafficCon["H"] & RidePunc["O"], RePoint["H"])

# 15. Nếu (Khoảng cách là Trung bình) VÀ (Giao thông là Trung bình) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Trung bình.
rule15 = ctrl.Rule(RideDistance["M"] & TrafficCon["M"] & CusRate["G"], RePoint["M"])

# 16. Nếu (Xếp hạng của Khách hàng là Kém) VÀ (Đúng giờ là Trễ), THÌ Điểm thưởng là Không có.
rule16 = ctrl.Rule(CusRate["P"] & RidePunc["L"], RePoint["N"])

# 17. Nếu (Khoảng cách là Rất xa) VÀ (Thời tiết xấu) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Cao.
rule17 = ctrl.Rule(RideDistance["VL"] & WeatherCon["B"] & CusRate["G"], RePoint["H"])

# 18. Nếu (Khoảng cách là Ngắn) VÀ (Xếp hạng của Khách hàng là Trung bình) VÀ (Đúng giờ là Đúng giờ), THÌ Điểm thưởng là Ít.
rule18 = ctrl.Rule(RideDistance["S"] & CusRate["A"] & RidePunc["O"], RePoint["F"])

# 19. Nếu (Khoảng cách là Dài) VÀ (Giao thông là Cao) VÀ (Đúng giờ là Trễ), THÌ Điểm thưởng là Ít.
rule19 = ctrl.Rule(RideDistance["L"] & TrafficCon["H"] & RidePunc["L"], RePoint["F"])

# 20. Nếu (Khoảng cách là Trung bình) VÀ (Thời tiết là Trung bình) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Trung bình.
rule20 = ctrl.Rule(RideDistance["M"] & WeatherCon["M"] & CusRate["G"], RePoint["M"])

# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6,
    rule7, rule8, rule9, rule10, rule11, rule12,
    rule13, rule14, rule15 , rule16, rule17, rule18, rule19, rule20
])

grab_system = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ
grab_system.input['RideDistance'] = 20    # Khoảng cách dài (giá trị thuộc "L")
grab_system.input['TrafficCon'] = 90      # Giao thông cao (giá trị thuộc "H")
grab_system.input['DemandLv'] = 90        # Nhu cầu cao (giá trị thuộc "H")
grab_system.input['WeatherCon'] = 1       # Thời tiết xấu (giá trị thuộc "B")
grab_system.input['CusRate'] = 5         # Đánh giá khách hàng tốt (giá trị thuộc "G")
grab_system.input['RidePunc'] = 85       # Đúng giờ sớm (giá trị thuộc "E")

# Tính toán
grab_system.compute()

# Xuất kết quả
print("Giá đi xe:", grab_system.output['Price'])
print("Điểm Thưởng:", grab_system.output['RePoint'])


# Hiển thị đồ thị kết quả
RideDistance.view()
TrafficCon.view()
DemandLv.view() 
WeatherCon.view()
CusRate.view()
RidePunc.view()
Price.view(sim=grab_system)
RePoint.view(sim=grab_system)


plt.show()
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
RideDistance = ctrl.Antecedent(np.arange(0, 51, 1), 'RideDistance')
TrafficCon = ctrl.Antecedent(np.arange(0, 101, 1), 'TrafficCon')
DemandLv = ctrl.Antecedent(np.arange(0, 101, 1), 'DemandLv')
WeatherCon = ctrl.Antecedent(np.arange(0, 6, 1), 'WeatherCon')
CusRate = ctrl.Antecedent(np.arange(1, 5.5, 0.5), 'CusRate')
RidePunc = ctrl.Antecedent(np.arange(0, 101, 1), 'RidePunc')

Price = ctrl.Consequent(np.arange(0, 11, 1), 'Price')
RePoint = ctrl.Consequent(np.arange(0, 11, 1), 'RePoint')

# Hàm thành viên cho RideDistance   # Khoảng cách
RideDistance["S"] = fuzz.trimf(RideDistance.universe, [0, 0, 3])   # Khoảng cách ngắn
RideDistance["M"] = fuzz.trimf(RideDistance.universe, [2, 5, 8])  # Khoảng cách trung bình
RideDistance["L"] = fuzz.trimf(RideDistance.universe, [6, 13, 20])  # Khoảng cách dài
RideDistance["VL"] = fuzz.trimf(RideDistance.universe, [15, 33, 50])  # Khoảng cách rất dài/xa

# Hàm thành viên cho TrafficCon     
TrafficCon["L"] = fuzz.trimf(TrafficCon.universe, [0, 0, 30]) # Giao thông thấp
TrafficCon["M"] = fuzz.trimf(TrafficCon.universe, [20, 45, 70]) # Giao thông trung bình
TrafficCon["H"] = fuzz.trimf(TrafficCon.universe, [60, 80, 100])    # Giao thông cao


# Hàm thành viên cho DemandLv   # Nhu cầu
DemandLv["L"] = fuzz.trimf(DemandLv.universe, [0, 0, 30])   # Nhu cầu thấp
DemandLv["M"] = fuzz.trimf(DemandLv.universe, [20, 45, 70])     # Nhu cầu trung bình
DemandLv["H"] = fuzz.trimf(DemandLv.universe, [60, 80, 100])   # Nhu cầu cao

# Hàm thành viên cho WeatherCon/ Điều kiện thời tiết
WeatherCon["B"] = fuzz.trimf(WeatherCon.universe, [0, 0, 2])     # bad
WeatherCon["M"] = fuzz.trimf(WeatherCon.universe, [2, 3, 4])     # Moderate
WeatherCon["G"] = fuzz.trimf(WeatherCon.universe, [3, 4, 5])     # Good

# Hàm thành viên cho CusRate / Đánh giá khách hàng
CusRate["P"] = fuzz.trimf(CusRate.universe, [1, 1, 2.5])    # Đánh giá kém
CusRate["A"] = fuzz.trimf(CusRate.universe, [2, 3, 4])   # Đánh giá trung bình
CusRate["G"] = fuzz.trimf(CusRate.universe, [3.5, 5, 5])    # Đánh giá tốt

# Hàm thành viên cho RidePunc / Đúng giờ
RidePunc["L"] = fuzz.trimf(RidePunc.universe, [0, 0, 50])   # Trễ
RidePunc["O"] = fuzz.trimf(RidePunc.universe, [40, 60, 80]) # Đúng giờ
RidePunc["E"] = fuzz.trimf(RidePunc.universe, [70, 85, 100])# Sớm

# Hàm thành viên cho Price  # Giá
Price["L"] = fuzz.trimf(Price.universe, [0, 0, 3])  # Giá thấp
Price["M"] = fuzz.trimf(Price.universe, [3, 5, 7])  # Giá trung bình
Price["H"] = fuzz.trimf(Price.universe, [5, 7, 9]) # Giá cao
Price["VH"] = fuzz.trimf(Price.universe, [8, 10, 10])    # Giá rất cao

# Hàm thành viên cho RePoint    # Điểm thưởng
RePoint["N"] = fuzz.trimf(RePoint.universe, [0, 0, 2])  # Không có điểm thưởng
RePoint["F"] = fuzz.trimf(RePoint.universe, [3, 5, 7])  # Điểm thưởng ít
RePoint["M"] = fuzz.trimf(RePoint.universe, [5, 7, 9])  # Điểm thưởng trung bình
RePoint["H"] = fuzz.trimf(RePoint.universe, [7, 9, 10])  # Điểm thưởng cao


# Các luật grab
# 1. Nếu (Khoảng cách ngắn) VÀ (Giao thông thấp) VÀ (Nhu cầu thấp), THÌ Giá thấp.
rule1 = ctrl.Rule(RideDistance["S"] & TrafficCon["L"] & DemandLv["L"], Price["L"])

# 2. Nếu (Khoảng cách ngắn) VÀ (Giao thông trung bình) VÀ (Nhu cầu cao), THÌ Giá trung bình.
rule2 = ctrl.Rule(RideDistance["S"] & TrafficCon["M"] & DemandLv["H"], Price["M"])

# 3. Nếu (Khoảng cách trung bình) VÀ (Giao thông cao) VÀ (Nhu cầu cao), THÌ Giá cao.
rule3 = ctrl.Rule(RideDistance["M"] & TrafficCon["H"] & DemandLv["H"], Price["H"])

# 4. Nếu (Khoảng cách dài) VÀ (Giao thông trung bình) VÀ (Thời tiết tốt), THÌ Giá trung bình.
rule4 = ctrl.Rule(RideDistance["L"] & TrafficCon["M"] & WeatherCon["G"], Price["M"])

# 5. Nếu (Khoảng cách dài) VÀ (Giao thông cao) VÀ (Thời tiết xấu), THÌ Giá cao.
rule5 = ctrl.Rule(RideDistance["L"] & TrafficCon["H"] & WeatherCon["B"], Price["H"])

# 6. Nếu (Khoảng cách rất xa) VÀ (Giao thông cao) VÀ (Nhu cầu cao), THÌ Giá cao.
rule6 = ctrl.Rule(RideDistance["VL"] & TrafficCon["H"] & DemandLv["H"], Price["H"])

# 7. Nếu (Khoảng cách trung bình) VÀ (Giao thông thấp) VÀ (Nhu cầu thấp), THÌ Giá trung bình.
rule7 = ctrl.Rule(RideDistance["M"] & TrafficCon["L"] & DemandLv["L"], Price["M"])

# 8. Nếu (Khoảng cách ngắn) VÀ (Lưu lượng giao thông cao) VÀ (Thời tiết xấu), THÌ Giá cao.
rule8 = ctrl.Rule(RideDistance["S"] & TrafficCon["H"] & WeatherCon["B"], Price["H"])

# 9. Nếu (Khoảng cách rất xa) VÀ (Thời tiết xấu), THÌ Giá rất cao.
rule9 = ctrl.Rule(RideDistance["VL"] & WeatherCon["B"], Price["H"])

# 10. Nếu (Khoảng cách trung bình) VÀ (Lưu lượng giao thông trung bình) VÀ (Thời tiết vừa phải), THÌ Giá trung bình.
rule10 = ctrl.Rule(RideDistance["M"] & TrafficCon["M"] & WeatherCon["M"], Price["M"])

# 11. Nếu (Đánh giá của khách hàng tốt) VÀ (Đúng giờ sớm), THÌ Điểm thưởng cao.
rule11 = ctrl.Rule(CusRate["G"] & RidePunc["E"], RePoint["H"])

# 12. Nếu (Đánh giá của khách hàng trung bình) VÀ (Đúng giờ đúng giờ), THÌ Điểm thưởng trung bình.
rule12 = ctrl.Rule(CusRate["A"] & RidePunc["O"], RePoint["M"])

# 13. Nếu (Đánh giá của khách hàng kém) VÀ (Đúng giờ muộn), THÌ Điểm thưởng không có.
rule13 = ctrl.Rule(CusRate["P"] & RidePunc["L"], RePoint["N"])

# 14. Nếu (Khoảng cách dài) VÀ (Lưu lượng giao thông cao) VÀ (Đi xe đúng giờ đúng giờ), THÌ Điểm thưởng cao.
rule14 = ctrl.Rule(RideDistance["L"] & TrafficCon["H"] & RidePunc["O"], RePoint["H"])

# 15. Nếu (Khoảng cách là Trung bình) VÀ (Giao thông là Trung bình) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Trung bình.
rule15 = ctrl.Rule(RideDistance["M"] & TrafficCon["M"] & CusRate["G"], RePoint["M"])

# 16. Nếu (Xếp hạng của Khách hàng là Kém) VÀ (Đúng giờ là Trễ), THÌ Điểm thưởng là Không có.
rule16 = ctrl.Rule(CusRate["P"] & RidePunc["L"], RePoint["N"])

# 17. Nếu (Khoảng cách là Rất xa) VÀ (Thời tiết xấu) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Cao.
rule17 = ctrl.Rule(RideDistance["VL"] & WeatherCon["B"] & CusRate["G"], RePoint["H"])

# 18. Nếu (Khoảng cách là Ngắn) VÀ (Xếp hạng của Khách hàng là Trung bình) VÀ (Đúng giờ là Đúng giờ), THÌ Điểm thưởng là Ít.
rule18 = ctrl.Rule(RideDistance["S"] & CusRate["A"] & RidePunc["O"], RePoint["F"])

# 19. Nếu (Khoảng cách là Dài) VÀ (Giao thông là Cao) VÀ (Đúng giờ là Trễ), THÌ Điểm thưởng là Ít.
rule19 = ctrl.Rule(RideDistance["L"] & TrafficCon["H"] & RidePunc["L"], RePoint["F"])

# 20. Nếu (Khoảng cách là Trung bình) VÀ (Thời tiết là Trung bình) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Trung bình.
rule20 = ctrl.Rule(RideDistance["M"] & WeatherCon["M"] & CusRate["G"], RePoint["M"])

# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6,
    rule7, rule8, rule9, rule10, rule11, rule12,
    rule13, rule14, rule15 , rule16, rule17, rule18, rule19, rule20
])

grab_system = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ
grab_system.input['RideDistance'] = 20    # Khoảng cách dài (giá trị thuộc "L")
grab_system.input['TrafficCon'] = 90      # Giao thông cao (giá trị thuộc "H")
grab_system.input['DemandLv'] = 90        # Nhu cầu cao (giá trị thuộc "H")
grab_system.input['WeatherCon'] = 1       # Thời tiết xấu (giá trị thuộc "B")
grab_system.input['CusRate'] = 5         # Đánh giá khách hàng tốt (giá trị thuộc "G")
grab_system.input['RidePunc'] = 85       # Đúng giờ sớm (giá trị thuộc "E")

# Tính toán
grab_system.compute()

# Xuất kết quả
print("Giá đi xe:", grab_system.output['Price'])
print("Điểm Thưởng:", grab_system.output['RePoint'])


# Hiển thị đồ thị kết quả
RideDistance.view()
TrafficCon.view()
DemandLv.view() 
WeatherCon.view()
CusRate.view()
RidePunc.view()
Price.view(sim=grab_system)
RePoint.view(sim=grab_system)


plt.show()