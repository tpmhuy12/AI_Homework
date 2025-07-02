import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
# Mức độ cấp bách 
Urgency = ctrl.Antecedent(np.arange(0, 101, 1), 'Urgency')
Urgency['L'] = fuzz.trimf(Urgency.universe, [0, 0, 30])      # Hiếm
Urgency['M'] = fuzz.trimf(Urgency.universe,[20, 50, 80])      # Thỉnh thoảng
Urgency['H'] = fuzz.trimf(Urgency.universe, [70, 100, 100])    # Thường xuyên

# Mức độ phức tạp
Complexity = ctrl.Antecedent(np.arange(0, 101, 1), 'Complexity')
Complexity['S'] = fuzz.trimf(Complexity.universe, [0, 0, 30])    # Thấp
Complexity['M'] = fuzz.trimf(Complexity.universe, [20, 50, 80])    # Trung bình
Complexity['C'] = fuzz.trimf(Complexity.universe, [70, 100, 100])  # Cao

# Mức ưu tiên phản hồi  - Biến đầu ra
Response_priority = ctrl.Consequent(np.arange(0, 101, 1), 'Response_priority')
Response_priority['L'] = fuzz.trimf(Response_priority.universe, [0, 0, 30])      # Thấp
Response_priority['N'] = fuzz.trimf(Response_priority.universe, [20, 50, 80])      # Trung bình
Response_priority['H'] = fuzz.trimf(Response_priority.universe, [70, 100, 100])    # Cao


# Các luật

rule1 = ctrl.Rule(Urgency['L'] & Complexity['S'], Response_priority['L'])  # Cấp bách thấp + Phức tạp đơn giản  →  Ưu tiên phản hồi THẤP
rule2 = ctrl.Rule(Urgency['M'] & Complexity['M'], Response_priority['N'])  # Cấp bách trung bình + Phức tạp vừa  →  Ưu tiên phản hồi TRUNG BÌNH
rule3 = ctrl.Rule(Urgency['H'] & Complexity['S'], Response_priority['H'])  # Cấp bách cao  + Phức tạp đơn giản  →  Ưu tiên phản hồi CAO
rule4 = ctrl.Rule(Urgency['H'] & Complexity['C'], Response_priority['H'])  # Cấp bách cao  + Phức tạp phức tạp  →  Ưu tiên phản hồi CAO (có thể chuyển người)
rule5 = ctrl.Rule(Urgency['L'] & Complexity['C'], Response_priority['N'])  # Cấp bách thấp + Phức tạp phức tạp  →  Ưu tiên phản hồi TRUNG BÌNH
rule6 = ctrl.Rule(Urgency['M'] & Complexity['S'], Response_priority['L'])  # Cấp bách trung bình + Phức tạp đơn giản  →  Ưu tiên phản hồi THẤP
rule7 = ctrl.Rule(Urgency['H'] & Complexity['M'], Response_priority['N'])  # Cấp bách cao  + Phức tạp vừa  →  Ưu tiên phản hồi TRUNG BÌNH


# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7
])

logistic = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ

logistic.input['Urgency'] =  8   # Mức độ khẩn cấp

logistic.input['Complexity'] =  9   # Mức độ phức tạp của yêu cầu


# Tính toán
logistic.compute()

# Xuất kết quả

if (logistic.output['Response_priority'] >= 8):
    print("Mức độ ưu tiên phản hồi cao: ", logistic.output['Response_priority'])
elif (logistic.output['Response_priority'] < 5):
    print("Mức độ ưu tiên phản hồi thấp: ", logistic.output['Response_priority'])
else:
    print("Mức độ ưu tiên phản hồi trung bình: ", logistic.output['Response_priority'])

# Hiển thị đồ thị kết quả
Urgency.view()
Complexity.view()


Response_priority.view(sim=logistic)

plt.show()
