import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
from matplotlib import pyplot as plt

# Khai báo các biến mờ
# Mật độ đơn hàng (Order Density)
OrderDensity = ctrl.Antecedent(np.arange(0, 11, 1), 'OrderDensity')
OrderDensity['L'] = fuzz.trimf(OrderDensity.universe, [0, 0, 5])      # Thấp
OrderDensity['M'] = fuzz.trimf(OrderDensity.universe, [2, 5, 8])      # Trung bình
OrderDensity['H'] = fuzz.trimf(OrderDensity.universe, [5, 10, 10])    # Cao

# Mức độ khẩn cấp giao hàng (Delivery Urgency)
DeliveryUrgency = ctrl.Antecedent(np.arange(0, 11, 1), 'DeliveryUrgency')
DeliveryUrgency['L'] = fuzz.trimf(DeliveryUrgency.universe, [0, 0, 5])    # Thấp
DeliveryUrgency['M'] = fuzz.trimf(DeliveryUrgency.universe, [2, 5, 8])    # Trung bình
DeliveryUrgency['H'] = fuzz.trimf(DeliveryUrgency.universe, [5, 10, 10])  # Cao

# Tải trọng hiện tại của tài xế (Driver's Current Load)
DriverLoad = ctrl.Antecedent(np.arange(0, 11, 1), 'DriverLoad')
DriverLoad['L'] = fuzz.trimf(DriverLoad.universe, [0, 0, 5])      # Thấp
DriverLoad['M'] = fuzz.trimf(DriverLoad.universe, [2, 5, 8])      # Trung bình
DriverLoad['H'] = fuzz.trimf(DriverLoad.universe, [5, 10, 10])    # Cao

# Tình trạng giao thông (Traffic Conditions)
TrafficCon = ctrl.Antecedent(np.arange(0, 11, 1), 'TrafficCon')
TrafficCon['L'] = fuzz.trimf(TrafficCon.universe, [0, 0, 5])      # Thấp
TrafficCon['M'] = fuzz.trimf(TrafficCon.universe, [2, 5, 8])      # Trung bình
TrafficCon['H'] = fuzz.trimf(TrafficCon.universe, [5, 10, 10])    # Cao

# Lợi nhuận trên mỗi lần giao hàng (Profit Per Delivery)
ProfitPerDelivery = ctrl.Antecedent(np.arange(0, 11, 1), 'ProfitPerDelivery')
ProfitPerDelivery['L'] = fuzz.trimf(ProfitPerDelivery.universe, [0, 0, 5])      # Thấp
ProfitPerDelivery['M'] = fuzz.trimf(ProfitPerDelivery.universe, [2, 5, 8])      # Trung bình
ProfitPerDelivery['H'] = fuzz.trimf(ProfitPerDelivery.universe, [5, 10, 10])    # Cao

# Số lượng đơn hàng cần kết hợp (Number of Orders to Combine) - Biến đầu ra
NumOrders = ctrl.Consequent(np.arange(0, 11, 1), 'NumOrders')
NumOrders['L'] = fuzz.trimf(NumOrders.universe, [0, 0, 5])      # Ít
NumOrders['M'] = fuzz.trimf(NumOrders.universe, [2, 5, 8])      # Trung bình
NumOrders['H'] = fuzz.trimf(NumOrders.universe, [5, 10, 10])    # Nhiều

# Ưu tiên giao hàng (Delivery Priority) - Biến đầu ra
DeliveryPriority = ctrl.Consequent(np.arange(0, 11, 1), 'DeliveryPriority')
DeliveryPriority['L'] = fuzz.trimf(DeliveryPriority.universe, [0, 0, 5])      # Thấp
DeliveryPriority['M'] = fuzz.trimf(DeliveryPriority.universe, [2, 5, 8])      # Trung bình
DeliveryPriority['H'] = fuzz.trimf(DeliveryPriority.universe, [5, 10, 10])    # Cao

# Các luật shopee
# Luật kết hợp đơn hàng:
# 1. Nếu (Mật độ đơn hàng cao) VÀ (Tải trọng hiện tại của tài xế thấp) VÀ (Tình trạng giao thông thấp) 
#    Thì kết hợp nhiều đơn hàng (NumOrders cao).
rule1 = ctrl.Rule(OrderDensity['H'] & DriverLoad['L'] & TrafficCon['L'], NumOrders['H'])

# 2. Nếu (Mật độ đơn hàng trung bình) VÀ (Tình trạng giao thông cao) VÀ (Mức độ khẩn cấp giao hàng trung bình) 
#    Thì kết hợp một vài đơn hàng (NumOrders trung bình).
rule2 = ctrl.Rule(OrderDensity['M'] & TrafficCon['H'] & DeliveryUrgency['M'], NumOrders['M'])

# 3. Nếu (Tải trọng hiện tại của tài xế cao) VÀ (Mật độ đơn hàng cao) VÀ (Lợi nhuận trên mỗi lần giao hàng trung bình) 
#    Thì kết hợp một số đơn hàng (NumOrders trung bình).
rule3 = ctrl.Rule(DriverLoad['H'] & OrderDensity['H'] & ProfitPerDelivery['M'], NumOrders['M'])

# 4. Nếu (Mật độ đơn hàng thấp) VÀ (Mức độ khẩn cấp giao hàng cao) VÀ (Điều kiện giao thông trung bình) 
#    Thì kết hợp một vài đơn hàng (NumOrders trung bình).
rule4 = ctrl.Rule(OrderDensity['L'] & DeliveryUrgency['H'] & TrafficCon['M'], NumOrders['M'])

# 5. Nếu (Lợi nhuận trên mỗi lần giao hàng cao) VÀ (Mức độ khẩn cấp giao hàng cao) VÀ (Điều kiện giao thông cao) 
#    Thì kết hợp một vài đơn hàng (NumOrders trung bình).
rule5 = ctrl.Rule(ProfitPerDelivery['H'] & DeliveryUrgency['H'] & TrafficCon['H'], NumOrders['M'])

# Luật ưu tiên giao hàng:
# 6. Nếu (Mức độ khẩn cấp giao hàng cao) VÀ (Lợi nhuận trên mỗi lần giao hàng cao) 
#    Thì mức độ ưu tiên giao hàng cao (DeliveryPriority cao).
rule6 = ctrl.Rule(DeliveryUrgency['H'] & ProfitPerDelivery['H'], DeliveryPriority['H'])

# 7. Nếu (Mức độ khẩn cấp giao hàng trung bình) VÀ (Điều kiện giao thông trung bình) 
#    Thì mức độ ưu tiên giao hàng trung bình (DeliveryPriority trung bình).
rule7 = ctrl.Rule(DeliveryUrgency['M'] & TrafficCon['M'], DeliveryPriority['M'])

# 8. Nếu (Mức độ khẩn cấp giao hàng thấp) VÀ (Mật độ đơn hàng cao) VÀ (Lợi nhuận trên mỗi lần giao hàng thấp) 
#    Thì mức độ ưu tiên giao hàng thấp (DeliveryPriority thấp).
rule8 = ctrl.Rule(DeliveryUrgency['L'] & OrderDensity['H'] & ProfitPerDelivery['L'], DeliveryPriority['L'])

# Khởi tạo hệ thống và mô phỏng
control_system = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8
])

logistic = ctrl.ControlSystemSimulation(control_system)

# Đầu vào ví dụ
logistic.input['OrderDensity'] =  9   # Mật độ đơn hàng cao (giá trị thuộc "H")
logistic.input['DeliveryUrgency'] =  4   # Mức độ khẩn cấp giao hàng trung bình (giá trị thuộc "M")
logistic.input['DriverLoad'] = 2      # Tải trọng hiện tại của tài xế thấp (giá trị thuộc "L")
logistic.input['TrafficCon'] = 3   # Tình trạng giao thông trung bình (giá trị thuộc "M")
logistic.input['ProfitPerDelivery'] = 5       # Lợi nhuận trên mỗi lần giao hàng trung bình (giá trị thuộc "M")

# Tính toán
logistic.compute()

# Xuất kết quả
if(logistic.output['NumOrders'] >7 ):
    print("Cần kết hợp nhiều đơn hàng.")
elif(   logistic.output['NumOrders'] <=3  ):
    print("Cần kết hợp ít đơn hàng.")
else:
    print("Cần kết hợp một số đơn hàng.")

if(logistic.output['DeliveryPriority'] > 7 ):
    print("Ưu tiên giao hàng cao.")
elif(   logistic.output['DeliveryPriority'] <=3  ): 
    print("Ưu tiên giao hàng thấp.")
else:
    print("Ưu tiên giao hàng trung bình.")

print("Số lượng đơn hàng cần kết hợp: ", logistic.output['NumOrders'])
print("Ưu tiên giao hàng: ", logistic.output['DeliveryPriority'])


# Hiển thị đồ thị kết quả
OrderDensity.view()
DeliveryUrgency.view()
DriverLoad.view() 
TrafficCon.view()
ProfitPerDelivery.view()

NumOrders.view(sim=logistic)
DeliveryPriority.view(sim=logistic)

plt.show()