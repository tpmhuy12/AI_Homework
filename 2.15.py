import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
# Tần số truy câp trang web (Web Visit Frequency)
WVF = ctrl.Antecedent(np.arange(0, 11, 1), 'WVF')
WVF['R'] = fuzz.trimf(WVF.universe, [0, 0, 5])      # Hiếm
WVF['ST'] = fuzz.trimf(WVF.universe, [2, 5, 8])      # Thỉnh thoảng
WVF['A'] = fuzz.trimf(WVF.universe, [5, 10, 10])    # Thường xuyên

# Giá trị mua hàng trung bình (Average Purchase Value)
APV = ctrl.Antecedent(np.arange(0, 11, 1), 'APV')
APV['L'] = fuzz.trimf(APV.universe, [0, 0, 5])    # Thấp
APV['M'] = fuzz.trimf(APV.universe, [2, 5, 8])    # Trung bình
APV['H'] = fuzz.trimf(APV.universe, [5, 10, 10])  # Cao

# Mức độ tương tác (Engagement Level)
EL = ctrl.Antecedent(np.arange(0, 11, 1), 'EL')
EL['L'] = fuzz.trimf(EL.universe, [0, 0, 5])      # Thấp
EL['M'] = fuzz.trimf(EL.universe, [2, 5, 8])      # Trung bình
EL['H'] = fuzz.trimf(EL.universe, [5, 10, 10])    # Cao


# Mức độ chú ý tiếp  - Biến đầu ra
AttentionLv = ctrl.Consequent(np.arange(0, 11, 1), 'AttentionLv')
AttentionLv['VL'] = fuzz.trimf(AttentionLv.universe, [0, 0, 3])      # Rất thấp
AttentionLv['L'] = fuzz.trimf(AttentionLv.universe, [2, 3, 4])      # Thấp
AttentionLv['M'] = fuzz.trimf(AttentionLv.universe, [3, 4, 5])      # Trung bình
AttentionLv['H'] = fuzz.trimf(AttentionLv.universe, [4, 6, 8])    # Cao
AttentionLv['VH'] = fuzz.trimf(AttentionLv.universe, [8, 10, 10])  # Rất cao

# Các luật shopee

rule1 = ctrl.Rule(WVF['A'] & APV['H'] & EL['H'], AttentionLv['H'])  # Thường xuyên truy cập, giá trị mua cao, tương tác cao -> Chú ý cao
rule2 = ctrl.Rule(WVF['ST'] & APV['M'] & EL['M'], AttentionLv['M'])  # Thỉnh thoảng truy cập, giá trị mua trung bình, tương tác trung bình -> Chú ý trung bình
rule3 = ctrl.Rule(WVF['R'] or EL['L'], AttentionLv['VL'])  # Hiếm truy cập, giá trị mua thấp, tương tác thấp -> Chú ý thấp
rule4 = ctrl.Rule(WVF['R'] & APV['H'] & EL['H'], AttentionLv['M'])  # Hiếm truy cập, giá trị mua cao, tương tác cao -> Chú ý trung bình

# Các luật khác
rule5 = ctrl.Rule(WVF['ST'] & APV['L'] & EL['L'], AttentionLv['L'])  # Thỉnh thoảng truy cập, giá trị mua thấp, tương tác thấp -> Chú ý thấp
rule6 = ctrl.Rule(WVF['A'] & APV['M'] & EL['M'], AttentionLv['H'])  # Thường xuyên truy cập, giá trị mua trung bình, tương tác trung bình -> Chú ý cao
rule7 = ctrl.Rule(WVF['R'] & APV['M'] & EL['H'], AttentionLv['M'])  # Hiếm truy cập, giá trị mua trung bình, tương tác cao -> Chú ý trung bình

# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7
])

logistic = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ
logistic.input['WVF'] =  7   # Mật độ đơn hàng cao (giá trị thuộc "H")
logistic.input['APV'] =  9   # Mức độ khẩn cấp giao hàng trung bình (giá trị thuộc "M")
logistic.input['EL'] = 9      # Tải trọng hiện tại của tài xế thấp (giá trị thuộc "L")

# Tính toán
logistic.compute()

# Xuất kết quả

print("Mức độ chú ý: ", logistic.output['AttentionLv'])


# Hiển thị đồ thị kết quả
WVF.view()
APV.view()
EL.view() 

AttentionLv.view(sim=logistic)

plt.show()