""" 模拟社会
by waterfish
优化版本：重构代码结构，修复 bug，优化用户体验
"""
import random
import math

# ==================== 配置常量 ====================
# 人口配置
NF = 10  # 农民人口
NW = 5   # 工人人口
NB = 2   # 商人人口
NT = 2   # 税务官人口
NPL = 1  # 民生官员人口
NM = 1   # 军事官员人口
NTEA = 0 # 教师人口
NG = 1   # 总督人口

# 派系索引
TAX_OFFICER = 0
LIVELIHOOD_OFFICER = 1
MILITARY_OFFICER = 2
TEACHER = 3
GOVERNOR = 4

# 游戏配置
DEFAULT_YEAR = 100
INITIAL_SATISFACTION = 8.0
INITIAL_FOOD = 40.0
INITIAL_PRODUCT = 0.0
FOOD_CONSUMPTION = 10.0
PRODUCT_DEMAND = 6.0
PRODUCT_COST = 2.0

# ==================== 工具函数 ====================
def get_float_input(prompt, default=None, min_val=None, max_val=None):
    """获取浮点数输入，带验证"""
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            value = float(value)
            if min_val is not None and value < min_val:
                print(f"值不能小于{min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"值不能大于{max_val}")
                continue
            return value
        except ValueError:
            if default is not None:
                print(f"输入无效，使用默认值：{default}")
                return default
            print("请输入有效数字")

def get_int_input(prompt, default=None, min_val=None, max_val=None):
    """获取整数输入，带验证"""
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            value = int(value)
            if min_val is not None and value < min_val:
                print(f"值不能小于{min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"值不能大于{max_val}")
                continue
            return value
        except ValueError:
            if default is not None:
                print(f"输入无效，使用默认值：{default}")
                return default
            print("请输入有效整数")

def get_choice_input(prompt, choices, default=None):
    """获取选择输入"""
    while True:
        value = input(prompt).strip().lower()
        if not value and default is not None:
            return default
        if value in choices:
            return value
        print(f"请输入以下选项之一：{', '.join(choices)}")

# ==================== 类定义 ====================
class Person:
    """个人类"""
    def __init__(self, intelligence=50):
        self.intelligence = intelligence
        self.food = INITIAL_FOOD  # a1: 粮食
        self.product = INITIAL_PRODUCT  # a2: 产品
        self.satisfaction = INITIAL_SATISFACTION  # s: 满意度
        self.for_sale_food = 1.0  # bf: 要出售的粮食
        self.for_sale_product = 1.0  # bw: 要出售的产品
    
    def total_wealth(self, product_price=3):
        """计算总财富（粮食 + 产品*价格）"""
        return self.food + self.product * product_price


class Group:
    """群体类，管理一类人群"""
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.members = [Person(intelligence=random.gauss(50, 15)) for _ in range(size)]
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return iter(self.members)
    
    def __getitem__(self, index):
        return self.members[index]
    
    def get_total_food(self):
        return sum(m.food for m in self.members)
    
    def get_total_product(self):
        return sum(m.product for m in self.members)
    
    def get_avg_satisfaction(self):
        if not self.members:
            return 0
        return sum(m.satisfaction for m in self.members) / len(self.members)
    
    def get_poorest(self):
        """返回最穷的成员索引"""
        if not self.members:
            return -1
        return min(range(len(self.members)), key=lambda i: self.members[i].total_wealth())


class GameState:
    """游戏状态类"""
    def __init__(self):
        # 人口组
        self.farmers = Group(NF, "农民")
        self.workers = Group(NW, "工人")
        self.merchants = Group(NB, "商人")
        
        # 公务员组（税务官、民生官员、军事官员、教师、总督）
        self.ser_size = NT + NPL + NM + NTEA + NG
        self.civil_servants = Group(self.ser_size, "公务员")
        
        # 国库
        self.treasury = 0.0
        
        # 税率
        self.tax_rate_farmer = 0.05
        self.tax_rate_worker = 0.1
        self.tax_rate_merchant = 0.2
        
        # 公务员工资
        self.civil_salary = 20.0
        
        # 产品价格
        self.product_price = 2.02
        self.merchant_price_multiplier = [12.0, 12.0]  # 商人价位倍数
        
        # 运输成本
        self.transport_cost = 2.0
        
        # 游戏状态
        self.year = 0
        self.total_years = DEFAULT_YEAR
        self.disaster_factor = 0.0  # 天灾影响
        self.crime_count = 0
        
        # 外交状态
        self.diplomatic_state = 0  # 0:未探索，1:慷慨帝国，2:霸权帝国
        self.diplomatic_mood = 0
        self.war_mode = False
        self.war_year = 0
        self.total_military_spending = 0.0
        
        # 成就
        self.achievements = set()
    
    def print_status(self):
        """打印当前状态"""
        print(f"\n=== 第 {self.year} 年 ===")
        print(f"国库：{self.treasury:.1f}")
        print(f"农民满意度：{self.farmers.get_avg_satisfaction():.1f}")
        print(f"工人满意度：{self.workers.get_avg_satisfaction():.1f}")
        print(f"商人满意度：{self.merchants.get_avg_satisfaction():.1f}")
        print(f"公务员满意度：{self.civil_servants.get_avg_satisfaction():.1f}")


# ==================== 游戏逻辑函数 ====================
def calculate_disaster(game, year):
    """计算天灾/丰收影响"""
    if year <= 5:
        pa = random.random()
        if pa > 0.66:
            game.disaster_factor = -0.2
            print('改革春风吹满地！增产 20%')
        else:
            game.disaster_factor = 0
        return
    
    # 5 年后天灾系统
    px = 0.0
    pa = random.random()
    pdisas = 0.1
    pharvest = 0.2
    
    if year < 15:
        if 4 * pa > pdisas:
            game.disaster_factor = 0.2
            print("天灾来临，减产 20%")
        elif pa < 1 - pharvest:
            game.disaster_factor = -0.3
            print('粮食大丰收，洪水被赶跑！增产 30%')
    else:
        if pa < pdisas - px:
            game.disaster_factor = 0.8
            px += 0.05
            print('天灾蹂躏大地，减产 80%')
            if px > 0.04 and '天灾如影' not in game.achievements:
                print('获得成就：天灾如影，常伴吾形')
                game.achievements.add('天灾如影')
        elif pa < 3 * pdisas - px:
            game.disaster_factor = 0.5
            px += 0.03
            print('天灾扫过荒野，减产 50%')
        elif pa < 5 * pdisas - px:
            game.disaster_factor = 0.2
            px += 0.01
            print('天灾降临人间，减产 20%')
        elif pa > 1 - pharvest * 3 / 5:
            px = 0
            game.disaster_factor = -0.4
            print('百姓安居乐业，齐夸党的领导！增产 40%')
        else:
            px = 0
            game.disaster_factor = 0


def farmer_production(game):
    """农民生产阶段"""
    for i, farmer in enumerate(game.farmers):
        if -10 < farmer.satisfaction < 15:
            # 计算产量
            base_yield = 130 + 30 * (farmer.intelligence - 50) / 100
            actual_yield = base_yield * (1 - game.disaster_factor)
            farmer.for_sale_food = actual_yield
            
            # 收税
            tax = actual_yield * game.tax_rate_farmer
            game.treasury += tax
            farmer.food += actual_yield * (1 - game.tax_rate_farmer)
            
            # 计算可出售粮食（扣除储备和需求）
            reserve_need = 30  # 储备需求
            if farmer.food < 10:
                farmer.for_sale_food = 0
                farmer.satisfaction -= 5
            elif farmer.food < reserve_need:
                farmer.for_sale_food = 0
                farmer.satisfaction -= 2
            else:
                farmer.for_sale_food = farmer.food - reserve_need
                farmer.satisfaction += 0.5


def worker_production(game):
    """工人生产阶段"""
    for i, worker in enumerate(game.workers):
        if -10 < worker.satisfaction < 15:
            # 计算产品价格
            base_price = 15 + 3 * (worker.intelligence - 50) / 100
            
            # 生产产品
            if worker.food >= base_price * 2:
                worker.product += base_price
                worker.food -= 2 * base_price
            else:
                base_price = worker.food / 2
                worker.product += base_price
                worker.food = 0
            
            # 根据满意度决定出售量
            min_product = 2
            target_product = 6
            
            if 10 < worker.satisfaction < 15:
                min_product -= (worker.satisfaction - 10) * (worker.satisfaction - 15) / 3
                target_product -= (worker.satisfaction - 10) * (worker.satisfaction - 15)
            
            if worker.product < min_product:
                worker.for_sale_product = 0
                worker.product = 0
                worker.satisfaction -= 2
            elif worker.product < target_product:
                worker.for_sale_product = 0
                worker.product -= min_product
            else:
                worker.for_sale_product = worker.product - target_product
                worker.product = target_product
                worker.satisfaction += 0.5
            
            # 粮食不足时调整价格
            if worker.food < 30 and worker.for_sale_product > 0:
                needed_price = (30 - worker.food) / (worker.for_sale_product * (1 - game.tax_rate_worker))
                if needed_price > game.product_price:
                    game.product_price = needed_price


def merchant_buy_from_workers(game):
    """商人从工人处购买产品"""
    for i, worker in enumerate(game.workers):
        if worker.for_sale_product <= 0:
            continue
        
        j = i % NB  # 分配给对应商人
        merchant = game.merchants[j]
        
        # 工人获得粮食
        revenue = game.product_price * worker.for_sale_product * (1 - game.tax_rate_worker)
        worker.food += revenue
        
        # 商人支付粮食并获得产品
        cost = game.product_price * worker.for_sale_product
        merchant.food -= cost
        merchant.product += worker.product
        
        # 税收
        tax = game.product_price * worker.product * game.tax_rate_worker
        game.treasury += tax
        
        # 记录商人成本
        # 注意：原代码有 bug，这里修正
        if not hasattr(merchant, 'total_cost'):
            merchant.total_cost = 0
        merchant.total_cost += cost
        
        # 清空工人待售产品
        worker.for_sale_product = 0
        worker.product = 0  # 产品已卖出


def merchant_consume(game):
    """商人消耗产品"""
    for merchant in game.merchants:
        min_product = 2
        target_product = 6
        
        if 10 < merchant.satisfaction < 15:
            min_product -= (merchant.satisfaction - 10) * (merchant.satisfaction - 15) / 3
            target_product -= (merchant.satisfaction - 10) * (merchant.satisfaction - 15)
        
        if merchant.product < min_product:
            merchant.product = 0
            merchant.satisfaction -= 2
        elif merchant.product < target_product:
            merchant.product -= min_product
        else:
            merchant.product -= target_product
            merchant.satisfaction += 0.5


def civil_servant_buy(game):
    """公务员购买产品"""
    for i, cs in enumerate(game.civil_servants):
        if cs.food < 30:
            continue
        
        j = i % NB  # 分配给对应商人
        if j >= len(game.merchants):
            continue
        merchant = game.merchants[j]
        
        if merchant.product <= 0:
            continue
        
        # 计算需求量
        min_product = 6
        if 10 < cs.satisfaction < 15:
            min_product -= (cs.satisfaction - 10) * (cs.satisfaction - 15)
        elif 0 < cs.satisfaction <= 10:
            pass  # 保持基础需求
        else:
            # 满意度过高或过低，先从国库偷钱
            t = abs(cs.satisfaction - 7.5) - 7.5
            if 0.1 * game.treasury > 20 * t:
                t = 0.005 * game.treasury
            game.treasury -= 20 * t
            cs.food += 20 * t
        
        needed = min_product - cs.product
        if needed <= 0:
            continue
        
        # 计算可购买量
        max_afford = (cs.food - 30) / (1.1 * game.product_price)
        buy_amount = min(needed, max_afford, merchant.product)
        
        if buy_amount > 0:
            cost = buy_amount * 1.1 * game.product_price
            cs.food -= cost
            cs.product += buy_amount
            merchant.food += cost
            merchant.product -= buy_amount
            
            if not hasattr(merchant, 'total_revenue'):
                merchant.total_revenue = 0
            merchant.total_revenue += cost


def merchant_sell_to_farmers(game):
    """商人向农民出售产品"""
    price_multiplier = [10.0, 10.0]  # 初始价格倍数
    
    # 价格逐渐下降
    for k in range(1, 12):
        for j, merchant in enumerate(game.merchants):
            if price_multiplier[j] > 2:
                price_multiplier[j] -= 1
            else:
                price_multiplier[j] = 1.01
            
            for i, farmer in enumerate(game.farmers):
                if i % NB != j:
                    continue
                
                if farmer.for_sale_food <= 0 or merchant.product <= 0:
                    continue
                
                # 计算需求量
                min_product = 6
                target_product = 12.5  # 6 + 6.25
                
                if 10 < farmer.satisfaction < 15:
                    min_product -= (farmer.satisfaction - 10) * (farmer.satisfaction - 15)
                
                needed = min_product - farmer.product
                if needed <= 0:
                    continue
                
                # 计算价格
                if farmer.for_sale_food > 0:
                    food_price = farmer.for_sale_food / needed
                else:
                    continue
                
                sell_price = price_multiplier[j] * (game.product_price + game.transport_cost)
                
                if food_price >= sell_price:
                    buy_amount = min(needed, merchant.product)
                    cost = buy_amount * sell_price
                    
                    farmer.food -= cost
                    farmer.product += buy_amount
                    merchant.food += cost
                    merchant.product -= buy_amount
                    farmer.for_sale_food -= cost / sell_price
                    
                    if not hasattr(merchant, 'total_revenue'):
                        merchant.total_revenue = 0
                    merchant.total_revenue += cost


def calculate_merchant_tax(game):
    """计算商人税收"""
    for merchant in game.merchants:
        if not hasattr(merchant, 'total_revenue'):
            merchant.total_revenue = 0
        if not hasattr(merchant, 'total_cost'):
            merchant.total_cost = 0
        
        profit = merchant.total_revenue - merchant.total_cost
        if profit > 0:
            tax = profit * game.tax_rate_merchant
            merchant.food -= tax
            game.treasury += tax
        
        # 重置收支记录
        merchant.total_revenue = 0
        merchant.total_cost = 0


def pay_civil_salary(game):
    """支付公务员工资"""
    for cs in game.civil_servants:
        cs.food += game.civil_salary
        game.treasury -= game.civil_salary


def consume_food(game):
    """消耗粮食并更新满意度"""
    # 农民
    for farmer in game.farmers:
        # 补贴
        if farmer.food < FOOD_CONSUMPTION and farmer.satisfaction <= 2:
            subsidy = FOOD_CONSUMPTION - farmer.food
            farmer.food += subsidy
            game.treasury -= subsidy
        
        # 消耗
        if farmer.food < FOOD_CONSUMPTION:
            farmer.food = 0
            farmer.satisfaction -= 5
        elif farmer.food < 30:
            farmer.food -= FOOD_CONSUMPTION
            farmer.satisfaction -= 2
        else:
            farmer.food -= FOOD_CONSUMPTION
            farmer.satisfaction += 0.5
        
        # 产品消耗
        min_product = 2
        target_product = 6
        if 10 < farmer.satisfaction < 15:
            min_product -= (farmer.satisfaction - 10) * (farmer.satisfaction - 15) / 3
            target_product -= (farmer.satisfaction - 10) * (farmer.satisfaction - 15)
        
        if farmer.product < min_product:
            farmer.product = 0
            farmer.satisfaction -= 2
        elif farmer.product < target_product:
            farmer.product -= min_product
        else:
            farmer.product -= target_product
            farmer.satisfaction += 0.5
    
    # 工人
    for worker in game.workers:
        if worker.food < FOOD_CONSUMPTION and worker.satisfaction <= 2:
            subsidy = FOOD_CONSUMPTION - worker.food
            worker.food += subsidy
            game.treasury -= subsidy
        
        if worker.food < FOOD_CONSUMPTION:
            worker.food = 0
            worker.satisfaction -= 5
        elif worker.food < 30:
            worker.food -= FOOD_CONSUMPTION
            worker.satisfaction -= 2
        else:
            worker.food -= FOOD_CONSUMPTION
            worker.satisfaction += 0.5
    
    # 商人（无补贴）
    for merchant in game.merchants:
        if merchant.food < 0:
            # 粮食不足，卖出产品
            if merchant.food + 2 * merchant.product < 30:
                merchant.food += 2 * merchant.product
                merchant.product = 0
            else:
                delta = merchant.food
                merchant.food = 30
                merchant.product -= (30 - delta) / 2
        elif merchant.food < FOOD_CONSUMPTION:
            merchant.food = 0
            merchant.satisfaction -= 5
        elif merchant.food < 30:
            merchant.food -= FOOD_CONSUMPTION
            merchant.satisfaction -= 2
        else:
            merchant.food -= FOOD_CONSUMPTION
            merchant.satisfaction += 0.5
    
    # 公务员
    for cs in game.civil_servants:
        if cs.food < FOOD_CONSUMPTION:
            cs.food = 0
            cs.satisfaction -= 5
        elif cs.food < 30:
            cs.food -= FOOD_CONSUMPTION
            cs.satisfaction -= 2
        else:
            cs.food -= FOOD_CONSUMPTION
            cs.satisfaction += 0.5
        
        # 产品消耗
        min_product = 2
        target_product = 6
        if 10 < cs.satisfaction < 15:
            min_product -= (cs.satisfaction - 10) * (cs.satisfaction - 15) / 3
            target_product -= (cs.satisfaction - 10) * (cs.satisfaction - 15)
        
        if cs.product < min_product:
            cs.product = 0
            cs.satisfaction -= 2
        elif cs.product < target_product:
            cs.product -= min_product
        else:
            cs.product -= target_product
            cs.satisfaction += 0.5


def update_class_satisfaction(game):
    """更新阶级满意度（最穷的人和最穷阶级）"""
    # 农民
    if game.farmers.size > 0:
        poorest_idx = game.farmers.get_poorest()
        if poorest_idx >= 0:
            game.farmers[poorest_idx].satisfaction -= 0.4
    
    # 工人
    if game.workers.size > 0:
        poorest_idx = game.workers.get_poorest()
        if poorest_idx >= 0:
            game.workers[poorest_idx].satisfaction -= 0.4
    
    # 公务员
    if game.civil_servants.size > 0:
        poorest_idx = game.civil_servants.get_poorest()
        if poorest_idx >= 0:
            game.civil_servants[poorest_idx].satisfaction -= 0.4
    
    # 计算最穷阶级
    avg_wealth_farmer = game.farmers.get_avg_satisfaction()
    avg_wealth_worker = game.workers.get_avg_satisfaction()
    avg_wealth_ser = game.civil_servants.get_avg_satisfaction()
    
    wealths = [avg_wealth_farmer, avg_wealth_worker, avg_wealth_ser]
    min_wealth = min(wealths)
    max_wealth = max(wealths)
    
    if max_wealth > min_wealth + 10:
        diff = max_wealth - min_wealth
        poorest_class = wealths.index(min_wealth)
        
        penalty = 1.3 * (math.atan(40) + math.atan(2 * diff - 40))
        if poorest_class == 1 or poorest_class == 2:  # 工人或公务员
            penalty *= 1.2
        
        if poorest_class == 0:
            for farmer in game.farmers:
                farmer.satisfaction -= penalty
        elif poorest_class == 1:
            for worker in game.workers:
                worker.satisfaction -= penalty
        else:
            for cs in game.civil_servants:
                cs.satisfaction -= penalty


def update_crime_and_influence(game):
    """更新犯罪和满意度影响"""
    game.crime_count = 0
    
    groups = [game.farmers, game.workers, game.civil_servants]
    
    for group in groups:
        for i, person in enumerate(group):
            # 负面满意度影响周围人
            if -10 < person.satisfaction < 0:
                if i > 0:
                    group.members[i-1].satisfaction += 0.1 * person.satisfaction
                if i > 1:
                    group.members[i-2].satisfaction += 0.1 * person.satisfaction
            elif person.satisfaction < -10 or person.satisfaction > 20:
                j = abs(person.satisfaction - 2.5)
                if i > 0:
                    group.members[i-1].satisfaction += (j - 12.5)
                if i > 1:
                    group.members[i-2].satisfaction += (j - 12.5)
                game.crime_count += 1
    
    # 无犯罪时全员满意度微增
    if game.crime_count == 0:
        for farmer in game.farmers:
            farmer.satisfaction += 0.1
        for worker in game.workers:
            worker.satisfaction += 0.1
        for cs in game.civil_servants:
            cs.satisfaction += 0.1
        for merchant in game.merchants:
            merchant.satisfaction += 0.1


def handle_diplomacy(game):
    """处理外交事件"""
    if game.year <= 5:
        return
    
    if game.diplomatic_state == 0:
        p = random.random()
        bb = 0.15
        if p < 0.5 + bb:
            print('暂无外交风波')
        else:
            p = random.random()
            if p < 0.25:
                print('收到消息：我帝国物产丰盈，无所不有。国库 +1000')
                game.treasury += 2000
                print('成就：大国的见面礼')
                game.diplomatic_mood = 80
                game.diplomatic_state = 1  # 慷慨帝国
            else:
                print('收到消息：臣服于我，否则帝国的铁骑将荡平你的国家')
                game.diplomatic_mood = 75
                game.diplomatic_state = 2  # 霸权帝国
    
    elif game.diplomatic_state == 1:  # 慷慨帝国
        if game.diplomatic_mood > 60:
            print('你好我的朋友，看来我们需要一些友好交换')
            choice = get_choice_input('是否进贡（是/否）', ['是', '否'])
            if choice == '是':
                delta = 600 + 400 * random.random()
                game.treasury -= delta
                game.diplomatic_mood += 2
                print(f'国库失去 {delta:.1f}')
                
                if random.random() > 0.25:
                    print('我们的友谊长青')
                    delta = 600 + 800 * random.random()
                    game.treasury += delta
                    print(f'国库获得 {delta:.1f}')
            else:
                game.diplomatic_mood -= 5
                p = random.random()
                if p > 0.6:
                    print('我们的友谊不经考验吗？')
                elif p > 0.33:
                    print('我们仍留有回旋余地')
                else:
                    print('望你好自为之')
        else:
            print('我们已经解除外交关系')
            game.war_year += 1
            handle_war(game, 'generous')
    
    elif game.diplomatic_state == 2:  # 霸权帝国
        if game.diplomatic_mood > 60:
            print('你好，我们需要一些贡品')
            choice = get_choice_input('是否进贡（是/否）', ['是', '否'])
            if choice == '是':
                delta = 700 + 400 * random.random()
                game.treasury -= delta
                game.diplomatic_mood += 2
                print(f'国库失去 {delta:.1f}')
            else:
                game.diplomatic_mood -= 6
                p = random.random()
                if p > 0.6:
                    print('看来你们有自己的想法')
                elif p > 0.33:
                    print('你们服从性太差')
                else:
                    print('望你好自为之')
        else:
            print('我们已经解除外交关系')
            game.war_year += 1
            handle_war(game, 'aggressive')


def handle_war(game, enemy_type):
    """处理战争"""
    p = random.random()
    
    military = get_int_input('目前有开战风险，请输入军费投入（大于等于零）', default=0, min_val=0)
    game.total_military_spending += military
    
    if enemy_type == 'aggressive':
        try:
            info = get_int_input('按 1 显示军备情况', default=0)
            if info == 1:
                print(f'目前是开战的第{game.war_year}年')
                print(f'投入总军费{game.total_military_spending:.1f}')
        except:
            pass
    
    if p > game.diplomatic_mood / 60:
        game.diplomatic_mood -= 6
    else:
        print('你已经挑战了我们的底线，现在开战！')
        choice = get_choice_input('赔款（1），迎战（2）', ['1', '2'])
        
        if choice == '1':
            game.treasury -= 1200 + 200 * p
            game.diplomatic_mood += 8
        else:
            game.diplomatic_mood -= 6
            pwin = game.total_military_spending / (game.total_military_spending + 800 * game.war_year)
            
            if pwin > 0.8:
                print('轻取敌军，大捷！')
                reward = 1500 + 500 * p
                game.treasury += reward
                print(f'缴获战利品 {reward:.1f}')
                game.diplomatic_mood += 10
            elif pwin < 0.2:
                print('脆败')
                penalty = 1800 + 500 * p
                game.treasury -= penalty
                print(f'战争赔款 {penalty:.1f}')
                game.diplomatic_mood += 12
            else:
                print('激烈的战斗！')
                input('任意键继续')
                if pwin > p:
                    print('惨烈的胜利！')
                    reward = 700 + 600 * p
                    game.treasury += reward
                    print(f'国库获得 {reward:.1f}')
                elif pwin < p:
                    print('功亏一篑')
                    penalty = 650 + 600 * p
                    game.treasury -= penalty
                    print(f'赔款 {penalty:.1f}')
                    game.diplomatic_mood += 4
                else:
                    print('两败俱伤')
                    game.treasury -= 400
                    print('补给消耗 400')
                    game.diplomatic_mood += 5


def check_game_state(game):
    """检查游戏状态"""
    if game.crime_count >= 8:
        print(f'罪犯数为{game.crime_count}，游戏结束')
        return 'lose'
    
    if game.treasury >= 20000:
        print(f'国库储蓄为{game.treasury:.1f}，游戏胜利！')
        return 'win'
    
    if game.treasury <= -20000:
        print(f'国库负债为{-game.treasury:.1f}，游戏失败')
        return 'lose'
    
    return 'continue'


def print_status_detail(game):
    """打印详细状态"""
    while True:
        print("\n=== 详细状态 ===")
        print("输入想查看的量：满意度 (1)、粮食 (2)、产品 (3)、国库 (4)、罪犯 (5)")
        print("输入 e 继续游戏")
        
        choice = input("> ").strip().lower()
        
        if choice == 'e':
            break
        elif choice == '1' or choice == '满意度':
            print(f'农民：{[f"{m.satisfaction:.1f}" for m in game.farmers]}')
            print(f'工人：{[f"{m.satisfaction:.1f}" for m in game.workers]}')
            print(f'商人：{[f"{m.satisfaction:.1f}" for m in game.merchants]}')
            print(f'公务员：{[f"{m.satisfaction:.1f}" for m in game.civil_servants]}')
        elif choice == '2' or choice == '粮食':
            print(f'农民：{[f"{m.food:.1f}" for m in game.farmers]}')
            print(f'工人：{[f"{m.food:.1f}" for m in game.workers]}')
            print(f'商人：{[f"{m.food:.1f}" for m in game.merchants]}')
            print(f'公务员：{[f"{m.food:.1f}" for m in game.civil_servants]}')
        elif choice == '3' or choice == '产品':
            print(f'农民：{[f"{m.product:.1f}" for m in game.farmers]}')
            print(f'工人：{[f"{m.product:.1f}" for m in game.workers]}')
            print(f'商人：{[f"{m.product:.1f}" for m in game.merchants]}')
            print(f'公务员：{[f"{m.product:.1f}" for m in game.civil_servants]}')
        elif choice == '4' or choice == '国库':
            print(f'国库：{game.treasury:.1f}')
        elif choice == '5' or choice == '罪犯':
            print(f'罪犯：{game.crime_count}名')


def subsidy_class(game):
    """全面小康补贴"""
    choice = get_choice_input('输入你想补贴的阶级：农民 (1)，工人 (2)，商人 (3)，公务员 (4)', 
                              ['1', '2', '3', '4'], default='1')
    amount = get_int_input('输入补贴金额（默认 10）', default=10)
    
    if choice == '1':
        for farmer in game.farmers:
            farmer.food += amount
            game.treasury -= amount
    elif choice == '2':
        for worker in game.workers:
            worker.food += amount
            game.treasury -= amount
    elif choice == '3':
        for merchant in game.merchants:
            merchant.food += amount
            game.treasury -= amount
    elif choice == '4':
        for cs in game.civil_servants:
            cs.food += amount
            game.treasury -= amount
    
    print(f'已补贴{amount}粮食')


def get_tax_settings():
    """获取税率设置"""
    print("\n=== 税率设置 ===")
    tax_farmer = get_float_input("请输入农民税率 (0-1 之间): ", default=0.05, min_val=0, max_val=1)
    tax_worker = get_float_input("请输入工人税率 (0-1 之间): ", default=0.1, min_val=0, max_val=1)
    tax_merchant = get_float_input("请输入商人税率 (0-1 之间): ", default=0.2, min_val=0, max_val=1)
    civil_salary = get_float_input("请输入公务员工资: ", default=20, min_val=0)
    
    return tax_farmer, tax_worker, tax_merchant, civil_salary


# ==================== 主游戏循环 ====================
def main():
    """主函数"""
    print("=" * 50)
    print("欢迎来到模拟社会！")
    print("=" * 50)
    print("您好长官，我们的国家由您来领导。")
    print("目前公民分为农民、商人、工人、公务员四个阶级。")
    print("您需要调控税收来满足他们对于粮食和产品的需求，并充实自己的国库。")
    print("满意度过低或者过高可能会导致他们成为罪犯！")
    print("请沉着应对突发的天灾和战争")
    print("祝您好运！")
    print("=" * 50)
    
    # 初始设置
    tax_farmer, tax_worker, tax_merchant, civil_salary = get_tax_settings()
    
    game = GameState()
    game.tax_rate_farmer = tax_farmer
    game.tax_rate_worker = tax_worker
    game.tax_rate_merchant = tax_merchant
    game.civil_salary = civil_salary
    
    print(f"\n游戏将进行{game.total_years}年")
    print(f"运输成本为{game.transport_cost}")
    print(f"农民税率为{game.tax_rate_farmer}")
    print(f"工人税率为{game.tax_rate_worker}")
    print(f"商人税率为{game.tax_rate_merchant}")
    print(f"公务员工资为{game.civil_salary}")
    
    # 游戏主循环
    while game.year < game.total_years:
        game.year += 1
        game.treasury = 0  # 重置税收
        
        print(f"\n{'='*40}")
        print(f'现在是第{game.year}年')
        
        # 1. 天灾系统
        calculate_disaster(game, game.year)
        
        # 2. 生产阶段
        farmer_production(game)
        worker_production(game)
        
        # 3. 交易阶段
        merchant_buy_from_workers(game)
        merchant_consume(game)
        civil_servant_buy(game)
        merchant_sell_to_farmers(game)
        
        # 4. 税收和工资
        calculate_merchant_tax(game)
        pay_civil_salary(game)
        
        # 5. 消耗阶段
        consume_food(game)
        
        # 6. 满意度更新
        update_class_satisfaction(game)
        update_crime_and_influence(game)
        
        # 7. 外交和战争
        handle_diplomacy(game)
        
        # 8. 检查游戏状态
        result = check_game_state(game)
        if result != 'continue':
            break
        
        # 9. 打印状态
        game.print_status()
        if game.crime_count == 0:
            print('看起来国内一切正常')
        elif game.crime_count < 5:
            print('有一些隐患了看来是')
        else:
            print('山雨欲来了属于是')
        
        # 10. 查看详细状态
        print_status_detail(game)
        
        # 11. 每三年可修改税率
        if game.year % 3 == 1:
            choice = get_choice_input("每三年可以修改参数，是否修改？（是/否）", ['是', '否', 'y', 'n', 'yes', 'no'])
            if choice in ['是', 'y', 'yes']:
                tax_farmer, tax_worker, tax_merchant, civil_salary = get_tax_settings()
                game.tax_rate_farmer = tax_farmer
                game.tax_rate_worker = tax_worker
                game.tax_rate_merchant = tax_merchant
                game.civil_salary = civil_salary
        
        # 12. 每五年可补贴
        if game.year % 5 == 0:
            choice = get_choice_input('是否使用全面小康（给某个阶级补贴）？（是/否）', ['是', '否', 'y', 'n'])
            if choice in ['是', 'y']:
                subsidy_class(game)
        
        input('\n按任意键进入下一年...')
    
    print("\n" + "=" * 50)
    print("游戏结束！")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n游戏已退出")
    except Exception as e:
        print(f"\n发生错误：{e}")
        import traceback
        traceback.print_exc()
