import random

MAX_PLAYER_COUNT = 4
random.seed( 0 )

class CardType:
    null                = "<null>"
    landmark            = "Landmark"
    primary_industry    = "Primary Industry"
    secondary_industry  = "Secondary Industry"
    restaurant          = "Restaurant"
    major_establishment = "Major Establishment"
    
class CardSymbol:
    null     = "<null>"
    wheat    = "Wheat"
    cow      = "Cow"
    bread    = "Bread"
    cup      = "Cup"
    gear     = "Gear"
    landmark = "Landmark"
    factory  = "Factory"
    apple    = "Apple"


    
def d6_odds( dice, number ):
    dice_sides = 6
    if number in range(dice, dice * dice_sides + 1):
        if dice == 1:
            return (1.0 / pow( dice_sides, dice ) )
        elif dice == 2:
            if number > 7:
                number = 14 - number
            return float(number - 1) / pow( dice_sides, dice )
        elif dice == 3:
            if number > 10:
                number = 21 - number
            odds = (1,3,6,10,15,21,25,27)
            return odds[number-3] / 216.0
            
    return 0.0

def d6_odds_unit_test():
    print "Running d6_odds_unit_test...\n"
    print "d6_odds( 0, 0 ): " + str( d6_odds( 0, 0 ) )
    print "d6_odds( 0, 1 ): " + str( d6_odds( 0, 1 ) )
    print "d6_odds( 1, 1 ): " + str( d6_odds( 1, 1 ) )
    print "d6_odds( 1, 6 ): " + str( d6_odds( 1, 6 ) )
    print "d6_odds( 1, 9 ): " + str( d6_odds( 1, 9 ) )
    print "d6_odds( 2, 0 ): " + str( d6_odds( 2, 0 ) )
    print "d6_odds( 2, 1 ): " + str( d6_odds( 2, 1 ) )
    print "d6_odds( 2, 2 ): " + str( d6_odds( 2, 2 ) )
    print "d6_odds( 2, 6 ): " + str( d6_odds( 2, 6 ) )
    print "d6_odds( 2, 7 ): " + str( d6_odds( 2, 7 ) )
    print "d6_odds( 2, 8 ): " + str( d6_odds( 2, 8 ) )
    print "d6_odds( 2, 12 ): " + str( d6_odds( 2, 12 ) )
    print "d6_odds( 2, 13 ): " + str( d6_odds( 2, 13 ) )
    print "d6_odds( 2, 120 ): " + str( d6_odds( 2, 120 ) )
    print "d6_odds( 3, 0 ): " + str( d6_odds( 3, 0 ) )
    print "d6_odds( 3, 1 ): " + str( d6_odds( 3, 1 ) )
    print "d6_odds( 3, 2 ): " + str( d6_odds( 3, 2 ) )
    print "d6_odds( 3, 3 ): " + str( d6_odds( 3, 3 ) )
    print "d6_odds( 3, 10 ): " +  str( d6_odds( 3, 10 ) )
    print "d6_odds( 3, 11 ): " + str( d6_odds( 3, 11 ) )
    print "d6_odds( 3, 17 ): " + str( d6_odds( 3, 17 ) )
    print "d6_odds( 3, 18 ): " + str( d6_odds( 3, 18 ) )
    print "d6_odds( 3, 19 ): " + str( d6_odds( 3, 19 ) )
    print "d6_odds( 3, 200 ): " + str( d6_odds( 3, 200 ) )
    print "d6_odds( 4, 0 ): " + str( d6_odds( 4, 0 ) )
    print "d6_odds( 4, 4 ): " + str( d6_odds( 4, 4 ) )
    print ""

class Card:
    def __init__( self, name, type, symbol, cost, basepay, multiplier_symbol, minrange, maxrange ):
        self.name = name
        self.type = type
        self.symbol = symbol
        self.cost = cost
        self.basepay = basepay
        self.multiplier_symbol = multiplier_symbol
        self.minrange = minrange
        self.maxrange = maxrange

    def odds( self, dice ):
        odds = 0
        if self.minrange == self.maxrange:
            odds = d6_odds( dice, self.minrange )
        else:
            for i in range( self.minrange, self.maxrange + 1 ):
                odds = odds + d6_odds( dice, i )
                
        return odds

    def income( self, tableau, dice, players ):
        odds = self.odds( dice )
        multiplier = 0
        payout = self.payout( tableau )
        second_turn_multiplier = 1

        if self.type is CardType.primary_industry:
            multiplier = players
        elif self.type is CardType.secondary_industry:
            multiplier = 1
        elif self.type is CardType.restaurant:
            multiplier = players - 1
        elif self.type is CardType.major_establishment:
            # assume max payout
            if self is Cards.stadium:
                multiplier = players - 1
            elif self is Cards.tvStation:
                multiplier = 1
        
        if( tableau.has( Cards.amusementPark ) and tableau.has( Cards.trainStation ) and dice is 2 ):
            second_turn_multiplier = 7.0 / 6.0
            
        return odds * multiplier * payout * second_turn_multiplier
            
    def payout( self, tableau ):
        pay = self.basepay
        if tableau.has( Cards.shoppingMall ) and ( self.isCardSymbol( CardSymbol.bread ) or self.isCardSymbol( CardSymbol.cup ) ):
            pay = pay + 1
            
        if self.multiplier_symbol is not CardSymbol.null:
            pay = pay * tableau.countSymbols( self.multiplier_symbol )

        return pay
        
    def isCardName( self, name ):
        return self.name in name
        
    def isCardSymbol( self, symbol ):
        return self.symbol == symbol
        
    def typeString( self ):
        return CardType.getString( self.type )
        
    def symbolString( self ):
        return CardSymbol.getString( self.symbol )
        
    def inRange( self, roll ):
        return roll is min( max( roll, self.minrange ), self.maxrange )            

class Cards():
    wheatField              = Card( "Wheat Field",                CardType.primary_industry,      CardSymbol.wheat,    1,  1, CardSymbol.null,   1,  1 )
    ranch                   = Card( "Ranch",                      CardType.primary_industry,      CardSymbol.cow,      1,  1, CardSymbol.null,   2,  2 )
    bakery                  = Card( "Bakery",                     CardType.secondary_industry,    CardSymbol.bread,    1,  1, CardSymbol.null,   2,  3 )
    cafe                    = Card( "Cafe",                       CardType.restaurant,            CardSymbol.cup,      2,  1, CardSymbol.null,   3,  3 )
    convenienceStore        = Card( "Convenience Store",          CardType.secondary_industry,    CardSymbol.bread,    2,  3, CardSymbol.null,   4,  4 )
    forest                  = Card( "Forest",                     CardType.primary_industry,      CardSymbol.gear,     3,  1, CardSymbol.null,   5,  5 )
    stadium                 = Card( "Stadium",                    CardType.major_establishment,   CardSymbol.landmark, 6,  2, CardSymbol.null,   6,  6 )
    tvStation               = Card( "TV Station",                 CardType.major_establishment,   CardSymbol.landmark, 7,  5, CardSymbol.null,   6,  6 )
    businessCenter          = Card( "Business Center",            CardType.major_establishment,   CardSymbol.landmark, 8,  0, CardSymbol.null,   6,  6 )
    cheeseFactory           = Card( "Cheese Factory",             CardType.secondary_industry,    CardSymbol.factory,  5,  3, CardSymbol.cow,    7,  7 )
    furnitureFactory        = Card( "Furniture Factory",          CardType.secondary_industry,    CardSymbol.factory,  3,  3, CardSymbol.gear,   8,  8 )
    mine                    = Card( "Mine",                       CardType.primary_industry,      CardSymbol.gear,     6,  5, CardSymbol.null,   9,  9 )
    familyRestaurant        = Card( "Family Restaurant",          CardType.restaurant,            CardSymbol.cup,      3,  2, CardSymbol.null,   9, 10 )
    appleOrchard            = Card( "Apple Orchard",              CardType.primary_industry,      CardSymbol.wheat,    3,  3, CardSymbol.null,  10, 10 )
    fruitAndVegetableMarket = Card( "Fruit And Vegetable Market", CardType.secondary_industry,    CardSymbol.apple,    2,  2, CardSymbol.wheat, 11, 12 )
    trainStation            = Card( "Train Station",              CardType.landmark,              CardSymbol.landmark, 4,  0, CardSymbol.null,   0,  0 )
    shoppingMall            = Card( "Shopping Mall",              CardType.landmark,              CardSymbol.landmark, 10, 0, CardSymbol.null,   0,  0 )
    amusementPark           = Card( "Amusement Park",             CardType.landmark,              CardSymbol.landmark, 16, 0, CardSymbol.null,   0,  0 )
    radioTower              = Card( "Radio Tower",                CardType.landmark,              CardSymbol.landmark, 22, 0, CardSymbol.null,   0,  0 )
    
    @staticmethod
    def list():
        list = []
        list.append( Cards.wheatField )
        list.append( Cards.ranch )
        list.append( Cards.bakery )
        list.append( Cards.cafe )
        list.append( Cards.convenienceStore )
        list.append( Cards.forest )
        list.append( Cards.stadium )
        list.append( Cards.tvStation )
        list.append( Cards.businessCenter )
        list.append( Cards.cheeseFactory )
        list.append( Cards.furnitureFactory )
        list.append( Cards.mine )
        list.append( Cards.familyRestaurant )
        list.append( Cards.appleOrchard )
        list.append( Cards.fruitAndVegetableMarket )
        list.append( Cards.trainStation )
        list.append( Cards.shoppingMall )
        list.append( Cards.amusementPark )
        list.append( Cards.radioTower )
        
        return list
    
    @staticmethod
    def oneDieList():
        list = []
        for card in Cards.list():
            if card.maxrange <= 6:
                list.append( card )        
        return list
        
    @staticmethod
    def oneDieList():
        list = []
        for card in Cards.list():
            if card.minrange > 0 and card.maxrange <= 6:
                list.append( card )        
        return list
        
    @staticmethod
    def twoDieList():
        list = []
        for card in Cards.list():
            if card.minrange > 1:
                list.append( card )
        return list
        
    @staticmethod
    def blueCardList():
        list = []
        for card in Cards.list():
            if card.type is CardType.primary_industry:
                list.append( card )
        return list
       
    @staticmethod       
    def nonLandmarkList():
        list = []
        for card in Cards.list():
            if card.type is not CardType.landmark:
                list.append( card )
        return list

class CardUnitTest:
    def __init__( self ):
        self.tableau = Tableau()

    def printState( self, card ):
        print "Name: " + card.name
        print "Type: " + card.type
        print "Symbol: " + card.symbol
        print "Cost: " + str( card.cost )
        print "Base Pay: " + str( card.basepay ) 
        print "Min Range: " + str( card.minrange )
        print "Max Range: " + str( card.maxrange )
        print "Payout: " + str( card.payout( self.tableau ) )
        print "Income (1 die, 2 player): " + str( card.income( self.tableau, 1, 2 ) )
        print "Income (1 die, 4 player): " + str( card.income( self.tableau, 1, 4 ) )
        print "Income (2 die, 2 plyaer): " + str( card.income( self.tableau, 2, 2 ) )
        print "Income (2 die, 4 plyaer): " + str( card.income( self.tableau, 2, 4 ) )
        print ""

    def run( self ):
        print "Running CardUnitTest...\n"
        print "Print all cards:"
        for card in Cards.list():
            self.printState( card )
            
        print "\nPrint 1 die cards:"
        for card in Cards.oneDieList():
            self.printState( card )
    
class Supply:
    def __init__( self ):
        self.cards = dict()
        self.cards[ Cards.wheatField ] = 6
        self.cards[ Cards.ranch ] = 6
        self.cards[ Cards.bakery ] = 6
        self.cards[ Cards.cafe ] = 6
        self.cards[ Cards.convenienceStore ] = 6
        self.cards[ Cards.forest ] = 6
        self.cards[ Cards.stadium ] = MAX_PLAYER_COUNT
        self.cards[ Cards.tvStation ] = MAX_PLAYER_COUNT
        self.cards[ Cards.businessCenter ] = MAX_PLAYER_COUNT
        self.cards[ Cards.cheeseFactory ] = 6
        self.cards[ Cards.furnitureFactory ] = 6
        self.cards[ Cards.mine ] = 6
        self.cards[ Cards.familyRestaurant ] = 6
        self.cards[ Cards.appleOrchard ] = 6
        self.cards[ Cards.fruitAndVegetableMarket ] = 6
        self.cards[ Cards.trainStation ] = MAX_PLAYER_COUNT
        self.cards[ Cards.shoppingMall ] = MAX_PLAYER_COUNT
        self.cards[ Cards.amusementPark ] = MAX_PLAYER_COUNT
        self.cards[ Cards.radioTower ] = MAX_PLAYER_COUNT

    def has( self, card ):
        return card in self.cards and self.cards[ card ] > 0
        
    def count( self, card ):
        if card in self.cards.keys():
            return self.cards[ card ]
        return 0
        
    def take( self, card ):
        if not self.has( card ) or self.cards[ card ] < 1:
            print "Error: " + card.name + " is not in the supply."
        else:
            self.cards[ card ] = self.cards[ card ] - 1
    
class SupplyUnitTest:    
    def __init__( self ):
        self.supply = Supply()
    
    def printState( self, card ):
        print card.name + " in supply: " + str( self.supply.has( card ) )
        print card.name + " count in supply: " + str( self.supply.count( card ) )
        print ""

    def run( self ):
        print "Running SupplyUnitTest...\n"
        self.printState( Cards.wheatField )
        
        self.supply.take( Cards.wheatField )
        self.printState( Cards.wheatField )
        
        self.supply.take( Cards.wheatField )
        self.printState( Cards.wheatField )

class Tableau:
    def __init__( self ):
        self.cards = dict()
        self.cards[ Cards.wheatField ] = 1
        self.cards[ Cards.bakery ] = 1
        self.money = 3

    def resolveRedCards( self, roll ):
        income = 0
        for card in self.cards:
            if card.type is CardType.restaurant and card.inRange( roll ):
                income = income + ( self.cards[ card ] * card.payout( self ) )
        return income
        
    def resolveBlueCards( self, roll ):
        income = 0
        for card in self.cards:
            if card.type is CardType.primary_industry and card.inRange( roll ):
                income = income + ( self.cards[ card ] * card.payout( self ) )
        return income
        
    def resolveGreenCards( self, roll ):
        income = 0
        for card in self.cards:
            if card.type is CardType.secondary_industry and card.inRange( roll ):
                income = income + ( self.cards[ card ] * card.payout( self ) )
        return income        
        
    #TODO Need to handle 1 at a time
    def resolvePurpleCards( self, roll ):
        income = 0
        for card in self.cards:
            if card.type is CardType.major_establishment and card.inRange( roll ):
                print "Purple Cards not resolved."
                #income = income + ( self.cards[ card ] * card.payout( self ) )
        return income

    def cardCount( self, card ):
        if card in self.cards:
            return self.cards[ card ]
        return 0

    def countSymbols( self, symbol ):
        count = 0
        for card in self.cards:
            if card.symbol is symbol:
                count = count + self.cards[ card ]    
        return count

    def has( self, card ):
        return card in self.cards
        
    def gainCard( self, card ):
        if card in self.cards:
            self.cards[ card ] = self.cards[ card ] + 1
        else:
            self.cards[ card ] = 1
        
    def cardCount( self, card ):
        if card in self.cards:
            return self.cards[ card ]
        return 0
        
    def hasWon( self ):
        if self.has( Cards.trainStation ) and self.has( Cards.shoppingMall ) and self.has( Cards.amusementPark ) and self.has( Cards.radioTower ):
            return True
        return False
        
    def loseMoney( self, money ):
        if self.money - money < 0:
            lostMoney = self.money
            self.money = 0
        else:
            lostMoney = money
            self.money = self.money - money
        return lostMoney
    
    def gainMoney( self, money ):
        self.money = self.money + money
        return True
        
    def score( self ):
        score = self.money
        for card in self.cards:
            if card.type is CardType.landmark:
                score = score + card.cost
        return score
        
    def report( self ):
        for card in self.cards:
            print card.name + " count: " + str( self.cards[ card ] )
            
            
class TableauUnitTest:
    def __init__( self ):
        self.tableau = Tableau()
        self.supply = Supply()
        
    def printState( self ):
        print "Has Shopping Mall: " + str( self.tableau.has( Cards.shoppingMall ) )
        print "Money: " + str( self.tableau.money )
        print "Cards: "
        print self.tableau.cards

    def run( self ):
        print "Running TableauUnitTest...\n"
        self.tableau.money = 100
        self.printState()
        
        self.tableau.buyCard( Cards.stadium, self.supply )
        self.printState()
        
        self.tableau.buyCard( Cards.stadium, self.supply )
        self.printState()

class PlayerAIInterface:
    def __init__( self, name ):
        self.name = name
        
    def linkEngine( self, engine ):
        self.engine = engine

    def rollTwoDice( self ):
        return False
        
    def shouldReroll( self ):
        return False
    
    def buyCard( self ):
        return
        
        
class PlayerAI_ConvenienceStore( PlayerAIInterface ):
    def buyCard( self ):
        if self.engine.canBuy( self, Cards.convenienceStore ):
            return Cards.convenienceStore
        if self.engine.supply.has( Cards.convenienceStore ):
            return
            
        if self.engine.canBuy( self, Cards.bakery ):
            return Cards.bakery    
            
        if self.engine.canBuy( self, Cards.shoppingMall ):
            return Cards.shoppingMall
        if not self.engine.tableau[ self ].has( Cards.shoppingMall ):
            return
            
        if self.engine.canBuy( self, Cards.radioTower ):
            return Cards.radioTower
        if self.engine.canBuy( self, Cards.amusementPark ):
            return Cards.amusementPark        
        if self.engine.canBuy( self, Cards.trainStation ):
            return Cards.trainStation        
        return
        
        
class PlayerAI_JasonConvenienceStore( PlayerAIInterface ):
    def buyCard( self ):
        if self.engine.canBuy( self, Cards.shoppingMall ):
            return Cards.shoppingMall
        if self.engine.canBuy( self, Cards.convenienceStore ):
            return Cards.convenienceStore
            
        if self.engine.canBuy( self, Cards.radioTower ):
            return Cards.radioTower
        if self.engine.canBuy( self, Cards.amusementPark ):
            return Cards.amusementPark        
        if self.engine.canBuy( self, Cards.trainStation ):
            return Cards.trainStation        
            
        if self.engine.canBuy( self, Cards.wheatField ):
            return Cards.wheatField        
        if self.engine.canBuy( self, Cards.ranch ):
            return Cards.ranch                    
            
        return
        
class PlayerAI_Bakery( PlayerAIInterface ):
    def buyCard( self ):
        if self.engine.canBuy( self, Cards.bakery ):
            return Cards.bakery    
            
        if self.engine.canBuy( self, Cards.shoppingMall ):
            return Cards.shoppingMall
        if not self.engine.tableau[ self ].has( Cards.shoppingMall ):
            return
            
        if self.engine.canBuy( self, Cards.radioTower ):
            return Cards.radioTower
        if self.engine.canBuy( self, Cards.amusementPark ):
            return Cards.amusementPark        
        if self.engine.canBuy( self, Cards.trainStation ):
            return Cards.trainStation        
        return        
        
        
class PlayerAI_Blues( PlayerAIInterface ):
    def buyCard( self ):
        landmarkPriorityList = [ Cards.shoppingMall, Cards.radioTower, Cards.amusementPark, Cards.trainStation ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card   
        
        if self.engine.canBuy( self, Cards.wheatField ):
            return Cards.wheatField
        if self.engine.canBuy( self, Cards.ranch ):
            return Cards.ranch
        if self.engine.canBuy( self, Cards.forest ):
            return Cards.forest
        return
        
        
class PlayerAI_BluesPlusRed( PlayerAIInterface ):
    def buyCard( self ):
        landmarkPriorityList = [ Cards.shoppingMall, Cards.radioTower, Cards.amusementPark, Cards.trainStation ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card
           
        if self.engine.canBuy( self, Cards.cafe ):
            return Cards.cafe
        
        if self.engine.canBuy( self, Cards.wheatField ):
            return Cards.wheatField
        if self.engine.canBuy( self, Cards.ranch ):
            return Cards.ranch
        if self.engine.canBuy( self, Cards.forest ):
            return Cards.forest
        return      
        
class PlayerAI_OneDieSpectrum( PlayerAIInterface ):
    def buyCard( self ):
        landmarkPriorityList = [ Cards.shoppingMall, Cards.radioTower, Cards.amusementPark, Cards.trainStation ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card
            
        #set to a large number
        minCountCard = 1000000000000
        minCard = None
        for card in Cards.oneDieList():
            cardCount = self.engine.getCardCount( self, card )
            # exclude major establishments
            if cardCount < minCountCard and self.engine.canBuy( self, card ) and card.type is not CardType.major_establishment:
                minCountCard = cardCount
                minCard = card
        return minCard        
        
class PlayerAI_FurnitureFactory( PlayerAIInterface ):
    def rollTwoDice( self ):
        return True
        
    def buyCard( self ):
        landmarkPriorityList = [ Cards.trainStation, Cards.amusementPark, Cards.radioTower, Cards.shoppingMall ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card

        if self.engine.canBuy( self, Cards.forest ) and self.engine.getCardCount( self, Cards.forest ) < 3:
            return Cards.forest
                
        if self.engine.getCardCount( self, Cards.trainStation ) > 0:
            if self.engine.getCardCount( self, Cards.furnitureFactory ) < self.engine.getCardCount( self, Cards.mine ):
                if self.engine.canBuy( self, Cards.mine ) and self.engine.getCardCount( self, Cards.mine ) < 3:
                    return Cards.mine                        
                if self.engine.canBuy( self, Cards.furnitureFactory ) and self.engine.getCardCount( self, Cards.furnitureFactory ) < 3:
                    return Cards.furnitureFactory
            else:
                if self.engine.canBuy( self, Cards.furnitureFactory ) and self.engine.getCardCount( self, Cards.furnitureFactory ) < 3:
                    return Cards.furnitureFactory                        
                if self.engine.canBuy( self, Cards.mine ) and self.engine.getCardCount( self, Cards.mine ) < 3:
                    return Cards.mine


class PlayerAI_Null( PlayerAIInterface ):
    def buyCard( self ):
        landmarkPriorityList = [ Cards.radioTower, Cards.amusementPark, Cards.shoppingMall, Cards.trainStation ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card

class PlayerAI_CheeseFactory( PlayerAIInterface ):
    def rollTwoDice( self ):
        return True
        
    def buyCard( self ):
        landmarkPriorityList = [ Cards.trainStation, Cards.amusementPark, Cards.radioTower, Cards.shoppingMall ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card
                
        if self.engine.canBuy( self, Cards.ranch ):
            return Cards.ranch
                
        if self.engine.getCardCount( self, Cards.trainStation ) > 0:
            if self.engine.canBuy( self, Cards.cheeseFactory ):
                return Cards.cheeseFactory
        
        

class PlayerAI_FruitAndVegetableMarket( PlayerAIInterface ):
    def rollTwoDice( self ):
        if self.engine.getCardCount( self, Cards.fruitAndVegetableMarket ) > 0:
            return True
        return False
        
    def buyCard( self ):
        landmarkPriorityList = [ Cards.trainStation, Cards.amusementPark, Cards.radioTower, Cards.shoppingMall ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card

        if self.engine.canBuy( self, Cards.wheatField ):
            return Cards.wheatField                
                
        if self.engine.getCardCount( self, Cards.trainStation ) > 0:
            if self.engine.getCardCount( self, Cards.fruitAndVegetableMarket ) < self.engine.getCardCount( self, Cards.appleOrchard ):
                if self.engine.canBuy( self, Cards.fruitAndVegetableMarket ):
                    return Cards.fruitAndVegetableMarket
                if self.engine.canBuy( self, Cards.appleOrchard ):
                    return Cards.appleOrchard
            else:
                if self.engine.canBuy( self, Cards.appleOrchard ):
                    return Cards.appleOrchard
                if self.engine.canBuy( self, Cards.fruitAndVegetableMarket ):
                    return Cards.fruitAndVegetableMarket
        
        
class PlayerAI_Random( PlayerAIInterface ):
    def rollTwoDice( self ):
        return True
        
    def buyCard( self ):        
        landmarkPriorityList = [ Cards.trainStation, Cards.amusementPark, Cards.radioTower, Cards.shoppingMall ]
        for card in landmarkPriorityList:
            if self.engine.canBuy( self, card ):
                return card

        i = 0
        nonLandmarkList = Cards.nonLandmarkList()
        while( self.engine.getMoney( self ) > 0 and i < 100):
            i = i + 1
            card = nonLandmarkList[ random.randrange( 0, len( nonLandmarkList ) ) ]
            if self.engine.canBuy( self, card ) and card.type is not CardType.major_establishment:
                return card
                
        return
        
def rollDice( dice, sides ):
    if dice is 1:
        roll = random.randrange( 1, sides )
    else:
        roll = random.randrange( 1, sides ) + rollDice( dice - 1, sides )
    return roll
                
def circularRange( start, end, length ):
    if start < 0 or end < 0 or length < 0:
        return
    if end <= start:
        list = range( start, length )
        list.extend( range( 0, min( end, length ) ) )
        return list
    else:
        return range( start, min( end, length ) )

def circularRangeUnitTest():
    print "Testing circularRange...\n"
    print circularRange( 3, 10, 20 )
    print circularRange( 3, 10, 6 )
    print circularRange( 10, 3, 20 )
    print circularRange( 5, 5, 10 )
    print circularRange( 1, 1, 4 )
    print circularRange( 4, 4, 4 )
    print circularRange( 5, 5, 4 )
    print circularRange( 6, 6, 4 )
    print circularRange( 1, 3, 4 )
    print circularRange( -1, 3, 4 )
    print circularRange( 1, -3, 4 )
    print circularRange( -1, -3, 4 )
    print circularRange( 4, 3, 4 )
    print circularRange( 6, 3, 4 )


class Engine:
    def __init__( self, AIPlayers ):              
        if len( AIPlayers ) < 2 or len( AIPlayers ) > MAX_PLAYER_COUNT:
            print "Error: invalid number of players."
        else:
            self.supply  = Supply()
            self.players = []
            self.tableau = dict()
            for playerAI in AIPlayers:
                self.players.append( playerAI )
                playerAI.linkEngine( self )
                self.tableau[ playerAI ] = Tableau()
            
    def resolveRoll( self, roll, currentPlayer ):
        # resolve Red cards
        startIndex = self.players.index( currentPlayer )
        for i in circularRange( startIndex + 1, startIndex, len( self.players ) ):
            if self.tableau[ currentPlayer ].money is 0:
                break;
            player = self.players[ i ]
            fee = self.tableau[ player ].resolveRedCards( roll )
            fee = self.tableau[ currentPlayer ].loseMoney( fee )
            self.tableau[ player ].gainMoney( fee )
        
        #resolve Blue cards
        for i in circularRange( startIndex, startIndex, len( self.players ) ):
            player = self.players[ i ]
            income = self.tableau[ player ].resolveBlueCards( roll )
            self.tableau[ player ].gainMoney( income )
        
        #resolve Green Cards
        income = self.tableau[ currentPlayer ].resolveGreenCards( roll )
        self.tableau[ currentPlayer ].gainMoney( income )
           
        #resolve Purple cards
        income = self.tableau[ currentPlayer ].resolvePurpleCards( roll )
        self.tableau[ currentPlayer ].gainMoney( income )
        
    def resolveBuy( self, player ):
        card = player.buyCard()
        tableau = self.tableau[ player ]
        
        if card:
            if self.canBuy( player, card ):
                self.supply.take( card )
                tableau.gainCard( card )
                tableau.loseMoney( card.cost )
                return True
            else:
                print "Error: cannot buy " + card.name
        return False
        
        
    def canBuy( self, player, card ):
        tableau = self.tableau[ player ]
        if card.symbol is CardSymbol.landmark and tableau.cardCount( card ) > 0:
            return False
        
        if card.cost <= tableau.money and self.supply.has( card ):
            return True
            
        return False
        
    def getCardCount( self, player, card ):
        tableau = self.tableau[ player ]
        return self.tableau[ player ].cardCount( card )
        
    def getMoney( self, player ):
        return self.tableau[ player ].money

    def printEndReport( self, winner ):
        print winner.name + " has won.\n"
        for player in self.players:
            print player.name
            print "Money: " + str( self.tableau[ player ].money )
            print "TS: " + str( self.tableau[ player ].cardCount( Cards.trainStation ) )
            print "SM: " + str( self.tableau[ player ].cardCount( Cards.shoppingMall ) )
            print "AM: " + str( self.tableau[ player ].cardCount( Cards.amusementPark ) )
            print "RT: " + str( self.tableau[ player ].cardCount( Cards.radioTower ) )
            print ""
            
    def tableauReports( self ):
        for player in self.players:
            print player.name
            self.tableau[ player ].report()
            print ""
        
    def run( self ):
        while( True ):
            for player in self.players:
                tableau = self.tableau[ player ]
                if tableau.has( Cards.trainStation ) and player.rollTwoDice():
                    roll = rollDice( 2, 6 )
                else:
                    roll = rollDice( 1, 6 )
                self.resolveRoll( roll, player )
                self.resolveBuy( player )
                #print player.name + " score is: " + str( tableau.score() ) + " money is: " + str( tableau.money )               
                if tableau.hasWon():
                    #self.printEndReport( player )
                    #self.tableauReports()
                    return player
            #print ""
            #one round only
            #break
        
    
print "Hello Machi Koro!\n"

#d6_odds_unit_test()
test = CardUnitTest()
test.run()
#test = SupplyUnitTest()
#test.run()
#test = TableauUnitTest()
#test.run()
#circularRangeUnitTest()

            
#PlayerAI_FurnitureFactory
#PlayerAI_OneDieSpectrum
#PlayerAI_BluesPlusRed
#PlayerAI_Blues
#PlayerAI_Bakery
#PlayerAI_ConvenienceStore
#PlayerAI_JasonConvenienceStore
#PlayerAI_CheeseFactory
#PlayerAI_FruitAndVegetableMarket

i = 0
MAX_RUNS = 0
TICKS_FRACTIONS = 20
wins = dict()
#playerAIs = [ PlayerAI_Random( "Player1" ), PlayerAI_Random( "Player2" ), PlayerAI_Random( "Player3" ), PlayerAI_Random( "Player4" ) ]
playerAIs = [ PlayerAI_JasonConvenienceStore( "Player1" ), PlayerAI_JasonConvenienceStore( "Player2" ) ]
for playerAI in playerAIs:
    wins[ playerAI ] = 0

while i < MAX_RUNS:    
    engine = Engine( playerAIs )
    winner = engine.run()
    wins[ winner ] = wins[ winner ] + 1
    i = i + 1
    if MAX_RUNS > TICKS_FRACTIONS and i % ( MAX_RUNS / TICKS_FRACTIONS ) is 0:
        print( "." ),
print ""    

for playerAI in playerAIs:
    print playerAI.name + " won " + str( wins[ playerAI ] ) + " games."
    
    

