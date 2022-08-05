# height:身高
# weight:体重
# labourStrength:劳动强度 0：卧床；1：轻体力；2：中体力；3：重体力
# gender:性别 0：女 1：男
# 返回值

def calculate(height, weight, labourStrength, gender):
    STATUS_LIST = [
        '消瘦',
        '正常',
        '肥胖',
    ]
    standardWeight = height - 105
    minWeight = standardWeight * 0.8
    maxWeight = standardWeight * 1.2
    userStatus = 1
    if weight < minWeight:
        userStatus = 0
    if weight > maxWeight:
        userStatus = 2
    levelList = [
        [20, 35, 40, 45],
        [15, 25, 35, 40],
        [15, 20, 30, 35]
    ]
    userLevel = levelList[userStatus][labourStrength]
    totalDailyCalories = userLevel * standardWeight
    CarbohydrateCalories = 0.575 * totalDailyCalories
    ProteinCalories = 0.175 * totalDailyCalories
    FatCalories = 0.225 * totalDailyCalories

    CaloriesforBreakfast = 0.2 * totalDailyCalories
    CarbohydrateforBreakfast = CaloriesforBreakfast * 0.575 / 4
    ProteinforBreakfast = CaloriesforBreakfast * 0.175 / 4
    FatforBreakfast = CaloriesforBreakfast * 0.225 / 9

    CaloriesforLunch = 0.4 * totalDailyCalories
    CarbohydrateforLunch = CaloriesforLunch * 0.575 / 4
    ProteinforLunch = CaloriesforLunch * 0.175 / 4
    FatforLunch = CaloriesforLunch * 0.225 / 9

    CaloriesforDinner = 0.4 * totalDailyCalories
    CarbohydrateforDinner = CaloriesforDinner * 0.575 / 4
    ProteinforDinner = CaloriesforDinner * 0.175 / 4
    FatforDinner = CaloriesforDinner * 0.225 / 9

    res = {
        'standardWeight': standardWeight,
        'BMI': BMI(height, weight),
        'userStatus': STATUS_LIST[userStatus],
        'totalDailyCalories': totalDailyCalories,
        'CarbohydrateCalories': CarbohydrateCalories,
        'ProteinCalories': ProteinCalories,
        'FatCalories': FatCalories,
        'breakfast': {
            'Calories': CaloriesforBreakfast,
            'Carbohydrate': CarbohydrateforBreakfast,
            'Protein': ProteinforBreakfast,
            'Fat': FatforBreakfast
        },
        'lunch': {
            'Calories': CaloriesforLunch,
            'Carbohydrate': CarbohydrateforLunch,
            'Protein': ProteinforLunch,
            'Fat': FatforLunch
        },
        'dinner': {
            'Calories': CaloriesforDinner,
            'Carbohydrate': CarbohydrateforDinner,
            'Protein': ProteinforDinner,
            'Fat': FatforDinner
        }
    }
    print(res)
    return res


def BMI(height, weight):
    bmi = weight / (height ** 2)
    return bmi
