"""
This file contains all the games and the commands for the economy
The file "casinovault.json" contains the token balence of users.
If a discord user has never used the bot before, they must first do ;balence in a text chanel.
"""


import discord
from discord import embeds
from discord.ext import commands
import asyncio
import random
import json
import datetime


class gamble(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def balance(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_account_data()

        chip_bal = users[str(user.id)]["chips"]

        em = discord.Embed(title = "{}'s chips".format(str(ctx.author.name)[:-2]))
        em.add_field(name='chips', value=chip_bal)
        await ctx.send(embed=em)

    async def open_account(self, user):

        with open('bot_cogs/casinovault.json', "r") as f:
            users = json.load(f)

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["chips"] = 100
        
        with open('bot_cogs/casinovault.json', "w") as f:
            json.dump(users, f)
        return True
    
    async def get_account_data(self):
        with open('bot_cogs/casinovault.json', "r") as f:
            users = json.load(f)
        return users

    
    @commands.command()
    async def void(self, ctx, *, amount=100):
        try:
            await self.open_account(ctx.author) 
            users = await self.get_account_data()
            user = ctx.author
            if users[str(user.id)]["chips"]<amount:
                em = discord.Embed(title='Invalid Amount', description='You do not have enough chips.')
                await ctx.send(embed=em)
                return
            users[str(user.id)]["chips"]-=amount
            with open('bot_cogs/casinovault.json', "w") as f:
                json.dump(users, f)
            title1='Chip Deletion'
            description1 = "voided {} chips.".format(amount)
        except:
            title1 = "Something Went Wrong"
            description1='Input a valid amount.'
        em1 = discord.Embed(title=title1, description=description1)
        await ctx.send(embed=em1)


    @commands.command()
    async def bal(self, ctx, *, person='89fsdj83h4fre54uin43vf'):
        give_member = '89fsdj83h4fre54uin43vf'
        await self.open_account(ctx.author) 
        users = await self.get_account_data()
        user = ctx.author
        user1 = str(user)
        if person == '89fsdj83h4fre54uin43vf':
            em = discord.Embed(title="{}'s balance".format(user1), description="chips: {}".format(users[str(user.id)]["chips"]))
            await ctx.send(embed=em)
        else:
            for member in ctx.guild.members:
                if member.name == person:
                    give_member = member
                    break
            if give_member == '89fsdj83h4fre54uin43vf':
                title1 = 'An Error Has Occured'
                description1 = 'user not found.'
            else:
                title1 = "{}'s balance".format(give_member.name)
                description1 = users[str(give_member.id)]["chips"]

            em = discord.Embed(title=title1, description=description1)
            await ctx.send(embed=em)


    @commands.command()
    async def steal(self, ctx, *, target="383wfebu8b4f3rnfi"):
        if str(target) == '383wfebu8b4f3rnfi':
            em = discord.Embed(title='An Eror Occured', description='Please specify a target.')
            await ctx.send(embed=em)
            return
        users = await self.get_account_data()
        user = ctx.message.author
        if isinstance(target, str)==False:
            em = discord.Embed(title='An Eror Occured', description='Please specify a target.')
            await ctx.send(embed=em)
            return

        for member in ctx.guild.members:
            if member.name == target:
                target = member
        if isinstance(target, str) == True:
            em = discord.Embed(title='An Error Occured', description='The target you have spesified is not in this server.')
            await ctx.send(embed=em)
            return
        user_chips = users[str(user.id)]["chips"]
        target_amount = users[str(target.id)]["chips"]
        if (target_amount/2)>user_chips:
            em1 = discord.Embed(title='An Error Occured', value="You must have chips equivilent to at least half of the target's total in order to attept a steal.")
            await ctx.send(embed=em1)
            return

        loss  = int((user_chips/2)+(target_amount/2))
        if loss > user_chips:
            loss = int(user_chips)

        em1 = discord.Embed(title='Steal Chips', description = "Steal | You are attempting to steal from {}, with a 50 percent chance of success. If you succeed, you will steal half of their chips. If you fail, you will lose half of your chips plus chips equivilent to half of the target's total. The target will gain chips equivilent to half of their total. Do you want to proceed? (y/n) ".format(target))
        em1.add_field(name='Potential Loss', value="{} chips".format(loss), inline=True)
        em1.add_field(name='Potential Gain', value="{} chips".format(int(target_amount/2)), inline=True)
        em1_send = await ctx.send(embed=em1)
        def player_check(m):
                if m.author == user:
                    return 'ys'
        try:
            msg = await self.client.wait_for('message', timeout=120.0, check=player_check)
        except asyncio.TimeoutError:
            await em1_send.delete()
            return
        msg1 = msg.content
        if msg1 != 'y':
            await em1_send.delete()
            return
        flip = random.randint(1, 2)
        if flip == 1:
            title1 = 'Steal | You Lost the Coin Flip!'
            description1 = "You lost {} chips and {} gained {} chips!".format(loss, target.name, int(target_amount/2))
            users[str(user.id)]["chips"]-=loss
            users[str(target.id)]["chips"]+=int(target_amount/2)
        else:
            title1 = 'Steal | You Won the Coin Flip!'
            description1 = "You gained {} chips and {} lost {} chips!".format(int(target_amount/2), target.name, int(target_amount/2))
            users[str(user.id)]["chips"]+=int(target_amount/2)
            users[str(target.id)]["chips"]-=int(target_amount/2)
        em2 = discord.Embed(title=title1, description=description1)
        await em1_send.delete()
        await ctx.send(embed=em2)

        with open('bot_cogs/casinovault.json', "w") as f:
            json.dump(users, f)

    @commands.command()
    async def daily(self, ctx):
        users = await self.get_account_data()
        user = ctx.message.author
        time = str(datetime.datetime.now())
        newtime = time[5:10]
        day = int(time[8:10])
        month = int(time[5:7])
        time1 = users[str(user.id)]["daily"]
        month1 = int(time1[0:2])
        day1 = int(time1[3:5])
        month_diff = abs(month-month1)
        day_diff = abs(day-day1)
        if day_diff == 0:
            if month_diff>0:
                pass
            else:
                em = discord.Embed(title='An Error Occured', description='You already claimed your daily, come back tomorrow!')
                await ctx.send(embed=em)
                return
        users[str(user.id)]["chips"]+=1000
        users[str(user.id)]["daily"]=newtime        
        em = discord.Embed(title='Daily', description='You have just claimed your 1000 daily chips, you now have {} chips!'.format(users[str(user.id)]["chips"]))
        await ctx.send(embed=em)

        with open('bot_cogs/casinovault.json', "w") as f:
            json.dump(users, f)




    @commands.command()
    async def leaderboard(self, ctx):
        users = await self.get_account_data()

        token_info = []
        for user in users:
            for member in ctx.guild.members:
                if str(member.id) == user:
                    token_info.append([users[str(user)]['chips'], member.name])
        
        token_info.sort(reverse=True)
        await ctx.send(token_info)

        em = discord.Embed(title='Bal Top', description = 'The top 5 riches people across all servers:')
        for i in range(5):
            em.add_field(name="{}".format(token_info[i][1]), value=token_info[i][0], inline=False)
        
        await ctx.send(embed=em)



    @commands.command()
    async def give(self, ctx, *, given_member='A98dfh5dui32fdsF82DF'):
        error_token = False
        error_description = ""
        give_member = 'A98dfh5dui32fdsF82DF'
        if given_member=='A98dfh5dui32fdsF82DF':
            error_token = True
            error_description = 'use ;give <user> <amount>'
        else:
            list1 = given_member.split(" ")
            if len(list1)>2:
                for i in range(1, len(list1)-1):
                    list1[0]+=" "
                    list1[0]+=list1[i]
                for i in range(len(list1)):
                    if list1[1] == list1[-1]:
                        break
                    list1.pop(1)
            list1[1] = int(list1[1])
            if list1[1]<0:
                error_token = True
                error_description = 'use ;give <user> <amount>'
            else:
                await self.open_account(ctx.author) 
                users = await self.get_account_data()
                user = ctx.author
                if list1[1]>users[str(user.id)]["chips"]:
                    error_token = True
                    error_description = 'You do not have enough chips.'
            if error_token == False:
                for member in ctx.guild.members:
                    if member.name == list1[0]:
                        give_member = member
                        break
                if give_member == 'A98dfh5dui32fdsF82DF':
                    error_token = True
                    error_description = 'User not found.'
        if error_token == True:
            em = discord.Embed(title='An Error has Occured', description = error_description)
            await ctx.send(embed=em)
            return
        users[str(user.id)]["chips"]-=list1[1]
        users[str(give_member.id)]["chips"]+=list1[1]
        em = discord.Embed(title='Chip Transfer', description = "{} gave {} {} chips!".format(user.name, give_member.name, list1[1]))
        await ctx.send(embed=em)

        with open('bot_cogs/casinovault.json', "w") as f:
            json.dump(users, f)




    @commands.command()
    async def bj(self, ctx, *, amount=-1):
        try:
            if amount<0:
                await ctx.send('please enter a valid amount: ;bj <amount>')
                return
        except:
            await ctx.send('An error has occured, please try again.')
            return

        await self.open_account(ctx.author) 
        users = await self.get_account_data()
        user = ctx.author
        if amount>users[str(user.id)]["chips"]:
            await ctx.send('You do not have enough chips')
            return
        users[str(user.id)]["chips"]-=amount

        channel = ctx.channel
        A = 11
        player_total = 0
        dealer_total = 0
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, A]
        face_cards = ['10', 'J', 'Q', 'K']
        suits = [':diamonds:', ':clubs:', ':hearts:', ':spades:']

        #Cheats
        dealer_undo_cheat = False
        dealer_ace_cheat = False
        player_ace_cheat = False
 
        convert = {
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: face_cards[random.randint(1, 4)-1],
            11: 'A'
        }
        #initial deal
        player_card_1 = cards[random.randint(1, 13)-1]
        player_card_2 = cards[random.randint(1, 13)-1]
        dealer_card_1 = cards[random.randint(1, 13)-1]
        dealer_card_2 = cards[random.randint(1, 13)-1]
        if dealer_ace_cheat == True:
            place_holder3 = random.randint(1, 2)
            if place_holder3 == 1:
                dealer_card_1 = A
            else:
                dealer_card_2 = A
        if player_ace_cheat == True:
            place_holder3 = random.randint(1, 2)
            if place_holder3 == 1:
                player_card_1 = A
            else:
                player_card_2 = A
        dealer_card_1_suit = suits[random.randint(1, 4)-3]
        player_cards = [player_card_1, player_card_2]
        dealer_cards = [dealer_card_1, dealer_card_2]
        player_cards_display = suits[random.randint(1, 4)-3]+str(convert[player_card_1]) + suits[random.randint(1, 4)-3] + str(convert[player_card_2])
        dealer_cards_display = dealer_card_1_suit+str(convert[dealer_card_1]) + suits[random.randint(1, 4)-3] + str(convert[dealer_card_2])
        place_holder4 = player_cards.count(11)
        dealer_total += dealer_card_1
        if place_holder4 >=2:
            player_cards[0] = 1
            player_total +=12
        else:
            player_total=player_card_1+player_card_2
        player_name = str(ctx.message.author)
        table_embed = discord.Embed(
            title="Blackjack | "+str(player_name)[:-2], 
            description="""The one who's closest to 21 wins. All cards count their own number up to 10. Ties go to the house.
            Use bj_hit to draw a new card
            use bj_stay to finish
            use bj_fold to surrender and obtain half of your initial bet
            """, 
            color=0x000000)
        table_embed.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
        table_embed.add_field(name="Dealer "+str(dealer_total), value=dealer_card_1_suit+convert[dealer_card_1]+" ?", inline=True)
        embed_msg = await ctx.send(embed=table_embed) #initial embed
        msg = False
        while msg == False:
            def check(m):
                if m.content == 'bj_hit' and m.channel == channel:
                        return 'bj_hit'
                elif m.content == 'bj_stay' and m.channel == channel:
                    return 'bj_stay'
                elif m.content == 'bj_fold' and m.channel == channel:
                    return 'bj_fold'
                else:
                    return ''
            msg = await self.client.wait_for('message', check=check)
            msg1 = str(msg.content)
            if msg1 == 'bj_fold':

                table_embed_fold = discord.Embed(
                    title="Blackjack | "+player_name+" | Fold", 
                    description = 'You have surrendered and recovered half of your bet ('+str(round(amount/2))+').',
                    color=0x000000)
                table_embed_fold.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
                table_embed_fold.add_field(name="Dealer "+str(dealer_card_1+dealer_card_2), value=dealer_card_1_suit+convert[dealer_card_1]+" ?", inline=True)
                await embed_msg.edit(embed=table_embed_fold)
                users[str(user.id)]["chips"]+=(int(amount/2))
                with open('bot_cogs/casinovault.json', "w") as f:
                    json.dump(users, f)
                return
            elif msg1 == 'bj_hit':
                while msg1 !='bj_stay':
                    if msg1 == 'bj_hit':
                        hit_card = cards[random.randint(1, 13)-1]
                        player_cards.append(hit_card)
                        player_cards_display += suits[random.randint(1, 4)-3]+convert[hit_card]
                        player_total += hit_card
                        if player_total >21:
                            if 11 in player_cards:
                                place_holder = player_cards.index(11)
                                player_cards[place_holder] = 1
                                player_total-=10
                            else:
                                table_embed_player_bust = discord.Embed(
                                title="Blackjack | "+player_name+" | You Lost! You exceeded 21.", 
                                color=0x000000)
                                table_embed_player_bust.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
                                table_embed_player_bust.add_field(name="Dealer ", value=dealer_card_1_suit+convert[dealer_card_1]+" ?", inline=True)
                                await embed_msg.edit(embed=table_embed_player_bust)
                                break  
                        table_embed_edit = discord.Embed(
                        title="Blackjack | "+player_name, 
                        description="""The one who's closest to 21 wins. All cards count their own number up to 10. Ties go to the house.
                        Use bj_hit to draw a new card
                        use bj_stay to finish
                        """, 
                        color=0x000000)
                        table_embed_edit.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
                        table_embed_edit.add_field(name="Dealer "+str(dealer_total), value=dealer_card_1_suit+convert[dealer_card_1]+" ?", inline=True)
                        await embed_msg.edit(embed=table_embed_edit)
                    def check(m):
                        if m.content == 'bj_stay' and m.channel == channel:
                            return 'bj_stay'
                        elif m.content == 'bj_hit' and m.channel == channel:
                            return 'bj_hit'
                    msg = await self.client.wait_for('message', check=check)
                    msg1 = str(msg.content)
                if player_total > 21:
                    with open('bot_cogs/casinovault.json', "w") as f:
                        json.dump(users, f)
                    return

        dealer_total-=dealer_card_1
        for card in dealer_cards:
            dealer_total+=card
        #checks for natural player blackjack
        if len(player_cards)==2 and player_total == 21 and dealer_total != 21:
            table_embed_edit = discord.Embed(
                title="Blackjack | "+player_name+" | BLACKJACK! You Won "+str(amount*2)+'.', 
            color=0x000000)
            table_embed_edit.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
            table_embed_edit.add_field(name="Dealer "+str(dealer_total), value=dealer_card_1_suit+str(dealer_card_1)+" ?", inline=True)
            await embed_msg.edit(embed=table_embed_edit)
            users[str(user.id)]["chips"]+=(int(amount * 2))
            with open('bot_cogs/casinovault.json', "w") as f:
                json.dump(users, f)
            return

        
        while dealer_total<17:
            card1 = cards[random.randint(1, 13)-1]
            dealer_cards.append(card1)
            dealer_total+=card1
            if dealer_total>21:
                if 11 in dealer_cards:
                    dealer_cards_display+=suits[random.randint(1, 4)-3]+convert[card1]
                    place_holder2 = dealer_cards.index(11)
                    dealer_cards[place_holder2] = 1
                    dealer_total -= 10
                elif dealer_undo_cheat == True:
                        dealer_total -= card1
                        dealer_cards.pop()
                        card1 = cards[random.randint(1, 13)-1]
                        dealer_total += card1
                        dealer_cards.append(card1)
                        dealer_cards_display+=suits[random.randint(1, 4)-3]+convert[card1]
                else:
                    dealer_cards_display+=suits[random.randint(1, 4)-3]+convert[card1]
                    table_embed_edit = discord.Embed(
                        title="Blackjack | "+player_name+" | You Won "+str(amount*2)+"! The dealer exceeded 21.", 
                        color=0x000000)
                    table_embed_edit.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
                    table_embed_edit.add_field(name="Dealer "+str(dealer_total), value=dealer_cards_display, inline=True)
                    await embed_msg.edit(embed=table_embed_edit)
                    users[str(user.id)]["chips"]+=(int(amount * 2))
                    with open('bot_cogs/casinovault.json', "w") as f:
                        json.dump(users, f)
                    break
            else:
                dealer_cards_display+=suits[random.randint(1, 4)-3]+convert[card1]
        if dealer_total >21:
            return
        
        if player_total>dealer_total:
            outcome_string = " | You Won! The dealer could not match you. You won "+str(amount*2)+'.'
            users[str(user.id)]["chips"]+=(int(amount * 2))
        elif dealer_total>player_total:
            outcome_string = " | You Lost! You did not match the dealer."
        else:
            outcome_string  = " | You Tied! You get your initial bet back."
            users[str(user.id)]["chips"]+=amount
        table_embed_edit = discord.Embed(
            title="Blackjack | "+player_name+outcome_string, 
            color=0x000000)
        table_embed_edit.add_field(name="You "+str(player_total), value=str(player_cards_display), inline=True)
        table_embed_edit.add_field(name="Dealer "+str(dealer_total), value=dealer_cards_display, inline=True)
        await embed_msg.edit(embed=table_embed_edit)
        with open('bot_cogs/casinovault.json', "w") as f:
            json.dump(users, f)







    @commands.command()
    #pregame setup
    async def poker(self, ctx, *, player2="1"): #first player named will be small blind, second will be big blind
        error_text = 'An Error Has Occured'; em3=discord.Embed(title=error_text)
        try:
            if player2=='1':
                em1 = discord.Embed(title=error_text, description='You cannot play by yourself. type ";poker_rules" to find the commands to play poker.')
                await ctx.send(embed=em1)
                return
            if player2 == str(ctx.message.author): #kfdskfkahfkjad move this ##############################
                await ctx.send('You cannot play with yourself.')
                return
        except:
            await ctx.send(em3)
            return
        await ctx.channel.send("15: ") ############################

        #creates the player list and finds the limit
        try:
            players = list(map(lambda p: p.strip(), player2.split(",")))
            print(players, players[0], int(players[0])) ################################
            limit = int(players[0])
            
        except:
            await ctx.channel.send("Please specify a valid betting limit.")
            return
        players.pop(0)
        try:
            if isinstance(limit, int)==False:
                em3.add_field(name="Error", value='Enter a valid limit', inline=True)
                await ctx.send(embed=em3)
                return
        except:
            em3.add_field(name="Error", value='Enter a valid limit', inline=True)
            await ctx.send(embed=em3)
            return
        if limit<100:
            em2 = discord.Embed(title=error_text, description='The minimum limit is 100 chips.')
            await ctx.send(embed=em2)
            return
        await self.open_account(ctx.author) 
        users = await self.get_account_data() 
        user = ctx.author
        if users[str(user.id)]["chips"]<limit:
            em4 = discord.Embed(title=error_text, description='You do not have enough chips.')
            await ctx.send(embed=em4)
        player_suit_1, player_suit_2 = '', ''
        pool = 0
        blind_counter, player_card_1, player_card_2, highest_card  = 0, 0, 0, 0
        call_cost, raise_cost = 10, 20
        game_stage = 0
        skip_2 = 0 #both players are the small and big blind so it skips them. This makes it so there isn't a pre-flop round
        small_blind_cost, big_blind_cost = 10, 20
        straight_counter, flush_counter, raise_effect, start_token, draw, check_token, token1, checking, all_in_effect, shuffle_counter, amount_token = False, False, False, False, False, False, False, False, False, False, False
        game_status, winning_token = True, True
        d_diamonds, d_clubs, d_hearts, d_spades, r_diamonds, r_clubs, r_hearts, r_spades = [], [], [], [], [], [], [], []
        all_in_players, all_cards, all_hand_value = [], [], []
        channel = ctx.channel
        raise_player, raise_amount, game_description = '', '', ''
        previous='none'
        game_number = str(random.randint(100000000, 999999999))
        actions = ['call', 'check', 'raise', 'fold', 'all in', 'all-in', 'bet']
        game_rounds = ['Pre-Flop', 'Flop', 'Turn', 'River', 'Showdown']
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        suits = [':diamonds:', ':clubs:', ':hearts:', ':spades:']
        combinations = ['high card', 'one pair', 'two pair', '3 of a kind', 'straight', 'flush', 'full house', '4 of a kind', 'straight flush', 'royal flush']
        suit_convert = {
            ':diamonds:': 0,
            ':clubs:': 1,
            ':hearts:': 2,
            ':spades:': 3
        }
        display_cards = {
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: '10',
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
            ':diamonds:': ':diamonds:',
            ':clubs:': ':clubs:',
            ':hearts:': ':hearts:',
            ':spades:': ':spades:'
        }

        community_card_1 = cards[random.randint(1, 13)-1]
        community_card_2 = cards[random.randint(1, 13)-1]
        community_card_3 = cards[random.randint(1, 13)-1]
        community_card_4 = cards[random.randint(1, 13)-1]
        community_card_5 = cards[random.randint(1, 13)-1]
        community_suit_1 = suits[random.randint(1, 4)-1]
        community_suit_2 = suits[random.randint(1, 4)-1]
        community_suit_3 = suits[random.randint(1, 4)-1]
        community_suit_4 = suits[random.randint(1, 4)-1]
        community_suit_5 = suits[random.randint(1, 4)-1]
        community_cards = [[community_suit_1, community_card_1], 
        [community_suit_2, community_card_2], 
        [community_suit_3, community_card_3], 
        [community_suit_4, community_card_4], 
        [community_suit_5, community_card_5]]
        for i in range(5):
            if community_cards[i][0] == ':diamonds:':
                d_diamonds.append(community_cards[i][1])
            elif community_cards[i][0] == ':clubs:':
                d_clubs.append(community_cards[i][1])
            elif community_cards[i][0] == ':hearts:':
                d_hearts.append(community_cards[i][1])
            elif community_cards[i][0] == ':spades:':
                d_spades.append(community_cards[i][1])
        while len(d_diamonds)>4 or len(d_clubs)>4 or len(d_hearts)>4 or len(d_spades)>4:
            community_suit_1 = suits[random.randint(1, 4)-1]
            community_suit_2 = suits[random.randint(1, 4)-1]
            community_suit_3 = suits[random.randint(1, 4)-1]
            community_suit_4 = suits[random.randint(1, 4)-1]
            community_suit_5 = suits[random.randint(1, 4)-1]
            d_diamonds, d_clubs, d_hearts, d_spades = [], [], [], []
            for i in range(5):
                if community_cards[i][0] == ':diamonds:':
                    d_diamonds.append(community_cards[i][1])
                elif community_cards[i][0] == ':clubs:':
                    d_clubs.append(community_cards[i][1])
                elif community_cards[i][0] == ':hearts:':
                    d_hearts.append(community_cards[i][1])
                elif community_cards[i][0] == ':spades:':
                    d_spades.append(community_cards[i][1])
        while community_card_1 == community_card_2 == community_card_3 == community_card_4 == community_card_5:
            community_card_1 = cards[random.randint(1, 13)-1]

        for g in range(len(players)):
            for member in ctx.guild.members:
                if member.name == players[g]:
                    players[g] = member
                    if limit>users[str(member.id)]["chips"]:
                        await ctx.send("{} does not have enough chips".format(member.name))
                        return
        
        for player in players: 
            if player not in ctx.guild.members:
                await ctx.send("error, a player invited is not in this server: {}".format(player))
                return
            
        print(players, " KHJDKHJLSSD") ########################################
        #Requires players to accept match
        player_str = str(ctx.message.author)[:-2]
        counter2=0
        for player in players:
            player_str+=" "+str(player)[:-2]
            counter2+=1
            if counter2 != len(players):
                player_str+=', '
        setup_embed = discord.Embed(
            description = 'Poker game #{} is setting up. Players will acept in the following order: {}'.format(game_number, player_str)
        )
        counter3 = False
        setup_message = await ctx.send(embed=setup_embed)

        #start of ready check
        for player in players:
            start_token = False
            setup_current_player = discord.Embed(
            description = 'currently waiting for {} to accept. Type "game accept" to accept the game invite, or "game decline" to reject the game'.format(str(player)[:-2])
            )
            if counter3 == False:
                counter3 = True
                player_accept_message = await ctx.send(embed=setup_current_player)
            else:
                await player_accept_message.edit(embed=setup_current_player)

            #repeated accepts
            while start_token != True:
                def player_check(m):
                    if m.content == 'game accept' and m.channel == channel:
                        return 'game accept'
                    else:
                        return 'invalid'

                msg = await self.client.wait_for('message', check=player_check) #maybe put a timeout here incase people don't respond
                msg1 = str(msg.content)
                if msg.author == player and str(msg1) == 'game accept':
                    start_token = True
                if msg.author == player and str(msg1) == 'game decline':
                    decline_em = discord.Embed(title='Game Decline', description='The game is cancelled because a player declined the game.')
                    await ctx.send(embed=decline_em)
                    return
                elif msg.author == player:
                    await ctx.send('type "game accept" in order to accept the match')
        setup_embed = discord.Embed(
            description = "All players have accepted the match! Game will begin momentarily."
        )
        await setup_message.edit(embed=setup_embed)
        await player_accept_message.delete()

        chips = {ctx.message.author: limit}
        initial_cards = {}
        for player1 in players:
            chips[player1] = limit
            users[str(player1.id)]["chips"]-=limit
        players.insert(0, ctx.message.author)

        #initial deal
        for player3 in players:
            if blind_counter<2:
                if blind_counter==0:
                    big_blind = player3 #small bind will be 5, big bind will be twice of small blind; 10.
                elif blind_counter ==1:
                    small_blind = player3
                else:
                    await ctx.send('blind selection error')
            blind_counter+=1

            player_card_1 = cards[random.randint(1, 13)-1]
            player_card_2 = cards[random.randint(1, 13)-1]
            player_suit_1 = suits[random.randint(1, 4)-1]
            player_suit_2 = suits[random.randint(1, 4)-1]
            player_cards = [[player_suit_1, player_card_1], [player_suit_2, player_card_2]]
            for i in range(2):
                if player_cards[i][0] == ':diamonds:' and player_cards[i][1] in d_diamonds:
                    shuffle_counter = True
                elif player_cards[i][0] == ':clubs:' and player_cards[i][1] in d_clubs:
                    shuffle_counter = True
                elif player_cards[i][0] == ':hearts:' and player_cards[i][1] in d_hearts:
                    shuffle_counter = True
                elif player_cards[i][0] == ':spades:' and player_cards[i][1] in d_spades:
                    shuffle_counter = True

            while shuffle_counter == True:
                player_card_1 = cards[random.randint(1, 13)-1]
                player_card_2 = cards[random.randint(1, 13)-1]
                player_suit_1 = suits[random.randint(1, 4)-1]
                player_suit_2 = suits[random.randint(1, 4)-1]
                shuffle_counter = False
                if player_cards[i][0] == ':diamonds:' and player_cards[i][1] in d_diamonds:
                    shuffle_counter = True
                elif player_cards[i][0] == ':clubs:' and player_cards[i][1] in d_clubs:
                    shuffle_counter = True
                elif player_cards[i][0] == ':hearts:' and player_cards[i][1] in d_hearts:
                    shuffle_counter = True
                elif player_cards[i][0] == ':spades:' and player_cards[i][1] in d_spades:
                    shuffle_counter = True

            initial_cards[player3] = player_cards
            
            player_card_string = ""
            for card in initial_cards[player3]:
                for card1 in card:
                    player_card_string += str(display_cards[card1])

            initial_card_embed = discord.Embed(
                title="Game #{} | You are Playing Texas Hold'em".format(game_number),
                description="Here are your cards: "+player_card_string
            )
            await player3.send(embed=initial_card_embed)
        
        chips[small_blind]-=small_blind_cost
        chips[big_blind]-=big_blind_cost
        pool = small_blind_cost + big_blind_cost
        
        await setup_message.delete()
        pregame_embed = discord.Embed(
            description = "Big blind will be {} and small blind will be {}.".format(big_blind, small_blind)
        )
        
        pre_game_mesage = await ctx.send(embed=pregame_embed)
        #main game ###########################################################################
        while game_status == True and game_stage < 4:
            if raise_effect != True:
                game_stage+=1
            if check_token == True:
                game_stage +=1
            game_round = game_rounds[game_stage-1]
            if raise_effect == False and game_stage>1:  #grants the ability to check at the start of each round
                checking = True
            current_community = ''
            if game_stage == 1: #pre-flop 
                current_community = '? ? ? ? ?'
            elif game_stage == 2: #flop
                try:
                    await pre_game_mesage.delete()
                except:
                    pass
                for i in range(3):
                    current_community+=display_cards[community_cards[i][0]]
                    current_community+=display_cards[community_cards[i][1]]
                    current_community+=" "
                for c in range(2):
                     current_community+="? "
            elif game_stage == 3: #turn
                for i in range(4):
                    current_community+=display_cards[community_cards[i][0]]
                    current_community+=display_cards[community_cards[i][1]]
                    current_community+=" "
                current_community+="? "
            else: #river and showdown
                for i in range(5):
                    current_community+=display_cards[community_cards[i][0]]
                    current_community+=display_cards[community_cards[i][1]]
                    current_community+=" "
            
            #resends this embed after every round.
            if raise_effect == False:
                try:
                    await game_message.delete()
                except:
                    pass
                game_embed = discord.Embed(
                description = "."
                )
                game_message = await channel.send(embed=game_embed)

            for player in players:###################################################################### start of players loop
                
                if skip_2<2:
                    skip_2+=1
                    continue
                if raise_effect==True and raise_player==player:
                    raise_effect = False
                    raise_player = ''
                    break
                if player in all_in_players: #doesn't give the player a turn if they all in
                    continue

                #checks how many community cards should be revealed
                if game_stage>1 and checking == True:
                    game_description = "Turn order will follow that listed above. You can currently fold, bet, check, or all in."
                elif all_in_effect == True:
                    game_description = 'Turn order will follow that listed above. You can currently all in or fold.'
                else:
                    game_description = "Turn order will follow that listed above. You can currently call, raise, or fold."
                game_embed = discord.Embed(
                    title='Poker Game #{} | {}'.format(game_number, player_str),
                    description = game_description
                    )

                game_embed.add_field(name='Previous Action', value=previous)
                game_embed.add_field(name='Current Turn:', value=str(player)[:-2], inline=True)
                game_embed.add_field(name='Pool Value:', value=pool, inline=True)
                game_embed.add_field(name='Game Stage', value=game_round, inline=True)
                if game_stage >1 and checking == True: #replaces the call option with the bet option
                    game_embed.add_field(name='Minimal Bet Cost', value=big_blind_cost, inline=True)
                elif all_in_effect == True:
                    game_embed.add_field(name='Call Cost', value=chips[player], inline=True) 
                else:
                    game_embed.add_field(name='Call Cost', value=call_cost, inline=True) 
                if game_stage>1 and checking == True: #replaces the raise option with all_in when the player can check
                    game_embed.add_field(name='All In Cost', value=chips[player], inline=True)
                elif all_in_effect == True:
                    pass
                else:
                    game_embed.add_field(name='Minimal Raise Cost', value=raise_cost, inline=True)

                game_embed.add_field(name='Community Cards', value=current_community, inline=True)
                game_embed.add_field(name='Your Chip Amount', value=chips[player], inline=True)
                await game_message.edit(embed=game_embed)

                while token1 != True:
                    def player_check(m):
                        if m.author == player and m.channel == channel:
                            return 'play'
                    try:
                        msg = await self.client.wait_for('message', timeout=180.0, check=player_check)
                    except asyncio.TimeoutError:
                        msg1 = 'fold'
                        token1 = True
                    msg1 = str(msg.content)
                    if msg.author == player:
                        if msg1 in actions:
                            token1 = True

                        if all_in_effect == True:
                            #
                            if checking == True:
                                await ctx.send('something has gone wrong; both checking and all_in_effect are active')
                            #
                            if msg1 == 'fold' or msg1 == 'all in' and msg1 =='call':
                                pass
                            else:
                                await ctx.send('You can only all in or fold right now.')
                                token1 = False
                                continue
                        #tests if the raise is a valid amount
                        if msg1[:5] == 'raise':
                            try:
                                raise_amount = int(msg1[6:])
                            except:
                                await ctx.send('Enter a valid raise amount')
                                token1 = False
                                continue
                            if raise_amount<(call_cost*2):
                                await ctx.send('enter a valid raise amount (minimal of 2x call cost)')
                                token1 = False
                                continue
                        #tests if a bet is valid
                        if msg1[:3] == 'bet':
                            if checking == False:
                                await ctx.send('you cannot bet right now')
                                token1 = False
                                continue
                            else:
                                bet_amount = int(msg1[4:])
                                if bet_amount<big_blind_cost:
                                    await ctx.send('ender a bet cost at least equivalent to the big blind')
                                    token1 = False
                                    continue
                        #checks if have the option to check
                        if msg1 == 'check' and checking == False:
                                token1 = False
                                await ctx.send('you cannot check right now')
                                continue
                        #checks if the player input a valid command when checking is active
                        elif checking == True:
                            if msg1 == 'call' or msg1[:5] == 'raise':
                                token1 = False
                                await ctx.send('you can only bet, check, or fold right now.')
                                continue
                        #checks if the user has the necessary funds to peform an action
                        if msg1 == 'call' or msg1[:5] == 'raise' or msg1[:3] == 'bet':
                            if msg1 == 'call':
                                if 0>(chips[player]-call_cost):
                                    amount_token = True
                            if msg1[:5] == 'raise':
                                if 0>(chips[player]-raise_amount):
                                    amount_token = True
                            if msg1[:3] == 'bet':
                                if 0>(chips[player]-bet_amount):
                                    amount_token = True
                            if amount_token == True:
                                amount_token = False
                                token1 = False
                                await ctx.send('you do not have enough chips.')
                                continue
                                
                token1 = False
                if str(msg1) == 'fold':
                    previous = 'fold'
                    users[str(player.id)]["chips"]+=chips[player]
                    players.remove(player)
                elif str(msg1) == 'call':
                    if previous == 'all in':
                        pool += chips[player]
                        chips[player] = 0
                        previous = 'all in'
                        all_in_players.append(player)
                        all_in_effect=True
                    else:
                        chips[player]-=call_cost
                        pool += call_cost
                        previous='call'
                elif msg1[:5] == 'raise':
                    chips[player]-=raise_amount
                    pool+=raise_amount
                    previous = 'raise'
                    call_cost = raise_amount
                    raise_cost = raise_amount*2 
                    raise_player = player
                    raise_effect = True
                elif msg1[:3] == 'bet':
                    chips[player]-=bet_amount
                    pool+=bet_amount
                    previous = 'bet'
                    call_cost = bet_amount
                    raise_cost = bet_amount * 2
                    raise_player = player
                    raise_effect = True
                    checking = False
                elif msg1 == 'check':
                    previous = 'check'
                elif msg1 == 'all in' or msg1 == 'all-in': 
                    call_cost = -1
                    raise_cost = -1
                    raise_player = player
                    raise_effect = True
                    pool+=chips[player]
                    chips[player] = 0
                    previous = 'all in'
                    all_in_players.append(player)
                    all_in_effect == True
                    checking = False

                if len(players) == 1:
                    game_status = False
                    em = discord.Embed(title='{} won! They are the last player remaining.'.format(players[0]), description="They won {}!".format(pool))
                    await game_message.delete()
                    await ctx.send(embed=em)
                    users[str(player.id)]["chips"]+=chips[players[0]]
                    users[str(player.id)]["chips"]+=pool
                    break

            if game_stage == 4 and raise_effect == True: #this is a lazy way to fix the bug of betting/calling on river being broken
                check_token = True
                game_stage -= 1
        if game_status == True:
            for i in range(5):
                if community_cards[i][0] == ':diamonds:':
                    r_diamonds.append(community_cards[i][1])
                elif community_cards[i][0] == ':clubs:':
                    r_clubs.append(community_cards[i][1])
                elif community_cards[i][0] == ':hearts:':
                    r_hearts.append(community_cards[i][1])
                elif community_cards[i][0] == ':spades:':
                    r_spades.append(community_cards[i][1])

            #showdown
            for player in players:
                sudo_diamonds = r_diamonds.copy()
                sudo_clubs = r_clubs.copy()
                sudo_hearts = r_hearts.copy()
                sudo_spades = r_spades.copy()
                suit_container = [sudo_diamonds, sudo_clubs, sudo_hearts, sudo_spades]
                count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                suit_count = [0, 0, 0, 0]
                all_cards = []
                hand_value = 0
                pair_counter = 0
                three_counter = 0
                highest_card = 0
                kicker = 0
                flush_counter = False
                straight_counter = False
                hand = initial_cards[player]

                for c in range(5):
                    all_cards.append(community_cards[c])

                for c in range(2):
                    all_cards.append(hand[c])
                
                for c in range(7):          
                    count[all_cards[c][1]-2]+=1
                    suit_count[suit_convert[all_cards[c][0]]] +=1
            #game_rounds = ['Pre-Flop', 'Flop', 'Turn', 'River', 'Showdown']
                    if all_cards[c][1]>kicker:
                        kicker = all_cards[c][1]

                #checks for fluhses
                for c in range(4):
                    if suit_count[c]>4:
                        flush_cards = suit_container[c]
                        flush_counter = True
                        for i in range(7):
                            highest_card = max(suit_count[c])

                #tests for straights
                for c in range(len(count)):
                    try:
                        if count[c]>=1 and count[c+1]>=1 and count[c+2]>=1 and count[c+3]>=1 and count[c+4]>=1:
                            straight_cards = [c+2, c+3, c+4, c+5, c+6]
                            straight_counter = True
                            highest_card = c+6
                    except:
                        break

                #tests for straight flushes and royal flushes
                if straight_counter == True and flush_counter == True:
                    if 10 in flush_cards and 11 in flush_cards and 12 in flush_cards and 13 in flush_cards and 14 in flush_cards:
                        hand_value = 9
                        highest_card = 14
                    else:
                        for card in straight_cards:
                            if card not in flush_cards:
                                hand_value = 0
                                break
                            else:
                                hand_value = 8

                #tests for 4 of a kind, 3 of a kind, 2 and 1 pair
                for i in range(len(count)):
                    if count[i] == 4:
                        highest_card = i+2
                        hand_value = 7
                        break
                    if straight_counter == False and flush_counter == False:
                        if count[i] == 3:
                            three_counter +=1
                            highest_card = i+2
                        elif count[i] == 2:
                            pair_counter +=1
                            if three_counter == 0:
                                highest_card = i+2

                if hand_value<6:
                    if three_counter >=1 and pair_counter >=1 or three_counter>1:
                        hand_value = 6
                    elif flush_counter == True:
                        hand_value = 5
                    elif straight_counter == True:
                        hand_value = 4
                    elif three_counter >=1:
                        hand_value = 3
                    elif pair_counter >1:
                        hand_value = 2
                    elif pair_counter == 1:
                        hand_value = 1
                    else:
                        hand_value = 0
                
                all_hand_value.append([player, hand_value, highest_card, kicker])

            current_community = " "
            for i in range(5):
                        current_community+=display_cards[community_cards[i][0]]
                        current_community+=display_cards[community_cards[i][1]]
                        current_community+=" "
            all_hand_embeds = discord.Embed(title='Showdown!', description=current_community)
            winner_highest = 0
            winner_kicker = 0
            big = 0
            winner = ''
            for i in range(len(all_hand_value)):
                player_card_string = ""
                for card in initial_cards[all_hand_value[i][0]]:
                    for card1 in card:
                        player_card_string += str(display_cards[card1])

                all_hand_embeds.add_field(name=all_hand_value[i][0].name, value=player_card_string, inline=True)
                #all_hand_value[i][1] is their hand value, [i][2] is their highest card in thier hand, and [i][3] is the kicker.
                if all_hand_value[i][1] > big:
                    winning_token = True
                elif all_hand_value[i][1] == big:
                    if all_hand_value[i][2]<winner_highest:
                        pass
                    elif all_hand_value[i][2]>winner_highest:
                        winning_token =  True
                    else:
                        if all_hand_value[i][3]<winner_kicker:
                            pass
                        elif all_hand_value[i][3]>winner_kicker:
                            winning_token = True
                        else:
                            draw = True
                            draw_player = all_hand_value[i][0]
                if winning_token == True:
                    winning_token = False
                    winner_kicker = all_hand_value[i][3]
                    winner_highest = all_hand_value[i][2]
                    big = all_hand_value[i][1]
                    winner = all_hand_value[i][0]
                    draw = False

            if draw == False:
                player_card_string = ""
                for card in initial_cards[winner]:
                    for card1 in card:
                        player_card_string += str(display_cards[card1])
                users[str(winner.id)]["chips"]+=int(pool)

                last_embed = discord.Embed(
                    title='{} won the game! Winnings: {}'.format(winner.name, pool), description='Their Cards: {}  | Their Hand: {}'.format(player_card_string, combinations[big])
                )

            else:
                draw_player_str = str(draw_player.name)
                last_embed = discord.Embed(
                    title='Its a draw!',
                    description="it's a draw between {} and {}!".format(winner.name, draw_player_str)
                )
                users[str(winner.id)]["chips"]+=int(pool/2)
                users[str(draw_player.id)]["chips"]+=int(pool/2)
            await game_message.delete()
            await ctx.send(embed=all_hand_embeds)
            await ctx.send(embed=last_embed)
        for player in players:
            users[str(player.id)]["chips"]+=chips[player]
        
        #edits the storage json file
        with open('bot_cogs/casinovault.json', "w") as f:
            json.dump(users, f)




    @commands.command()
    async def poker_rules(self, ctx):
        how_to_play_message = discord.Embed(title="How to play Poker", color=discord.Colour.red(), description="""
Game Commands

Initiating the Game:
;poker (limit), (player2), (player3), (player4), (player5), (player6)
(limit) and (player2) is mandetory (you must play with at least one other player and you must set a betting limit)

once the game has been initiated, all players must type game accept in the order they are mentioned.

Possible commands in game: call, bet <amount>, raise <amount>, all in, fold


How to play Texas Hold'em:

The game initiator and the first player mentioned will be the small and big blinds respectivly. They will be forced to bet an amount.

There are 5 rounds; pre-flop, flop, turn, river, and showdown. Each player will be dealt 2 cards, and there will be 5 community cards that are
periodically revealed throughout the rounds. No community cards will be revealed during pre-flop, 3 will be revealed during flop, 4 during turn,
and the last one during river.

During the preflop, players must either fold, call and pay the chips equivilent to the big blind, or raise to at least twice the big cost of big blind.

In the following rounds to preflop, the first player must check, bet an amount equivalent to the big blind, or all in. After a player has bet, all subsequent
players must call, raise, all in, or fold. If the first player checks, the option to check and bet moves on to the next player. The round will pass without
any bets being made if all players choose to check.
        
In this poker game, players can all in on any of their turns after the pre-flop round. Players can all in regardless of the previous action or their current chip amount.
Play will not recieve anymore turns after choosing to all in, since they have no more possible actions.

All remaining players will compare hands and the player with the highest hand will win. The game will also end if all but one player has folded.

Lowest to Highest Hand Values:
High card, one pair, two pair, three of a kind, straight, flush, full house, four of a kind, straight flush, royal flush.

For more information, visit https://www.pokerstars.com/poker/games/texas-holdem/?no_redirect=1
This message will self-delete 3 minutes after being posted.

Invite me to other servers using: https://discord.com/api/oauth2/authorize?client_id=866733937115922443&permissions=8&scope=bot
""")    
        how_message = await ctx.send(embed=how_to_play_message)
        await asyncio.sleep(180)
        await how_message.delete()


    @commands.command()
    async def five_poker(self, ctx, *, player3='2'):
        display_cards = {
            2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A',
            ':diamonds:': ':diamonds:', ':clubs:': ':clubs:', ':hearts:': ':hearts:', ':spades:': ':spades:'
        }
        pin = False
        blind = 20 #control the blind here, the pool will be 2x of blind since 2 players
        pool = blind * 2
        channel = ctx.channel
        error_em = discord.Embed(title='An Error Occured')
        player1 = ctx.author #important variable;
        fold_player = 'none'
 #var that loops the game to allow the var game_stage to be effective
        game_stage = 0 #determines which stage the game is on, and thus excecutes the code that corresponds to the game stage

        #prepares variables and catches input errors
        if player3 == '2':
            error_em.add_field(name="Oppenent Error", value='You cannot play by yourself, please use ;poker5 <amount>, <name>')
            await ctx.send(embed=error_em)
            return
        list1 = player3.split(", ")
        player2 = list1[1]
        try:
            limit = int(list1[0])
            if limit<100:
                error_em.add_field(name="Bet Value Error", value='You must bet a minimum of 100 chips.')
                await ctx.send(embed=error_em)
                return
        except:
            error_em.add_field(name="Bet Value Error", value='Please bet a valid amount.')
            await ctx.send(embed=error_em)
            return
        for member in ctx.guild.members:
            if member.name == player2:
                player2 = member
                pin = True
        if pin == False:
            error_em.add_field(name="Opponent Error", value="{} is not in this server.".format(player2))
            await ctx.send(embed=error_em)
            return
        players = [player1, player2]
        users = await self.get_account_data()
        user = ctx.message.author
        for player in players:
            if users[str(player.id)]["chips"]<limit:
                error_em.add_field(name='Balance Error', value="{} does not have enough chips to play.".format(player))
                await ctx.send(embed=error_em)
                return
        

        #game accept system
        start_embed = discord.Embed(title='5 card poker | {}'.format(player2), description = 'you have been invited to a 5 card poker game by {}, with a {} chip stake! Type "game accept" to accept the match, or "game decline" to reject the game invite. This invite will expire in 60 seconds.'.format(player1.name, limit))
        start_embed_msg = await ctx.send(embed=start_embed)
        start_edit = discord.Embed(title='Game Accepted!', description='5 card poker game between {} and {} is setting up.'.format(player1, player2))
        def check(m):
            if m.author == player2 and m.channel == channel:
                return 'play'
        try:
            msg = await self.client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await start_embed_msg.delete()
            return
        msg1 = msg.content
        if msg1 != 'game accept':
            await start_embed_msg.delete()
            return
        await start_embed_msg.edit(embed=start_edit)
        #start of card system
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        suits = [':diamonds:', ':clubs:', ':hearts:', ':spades:']
        all_sets, split_sets = [], []
        previous = 'none'
        counter1 = 0
        players_cards = {}
        player_chips = {}
        bet_round, fold_token = True, False
        one_swap, two_swap = False, False
        card_str1, card_str2 = "", ""
        users[str(players[0].id)]["chips"]-=limit
        users[str(players[1].id)]["chips"]-=limit
        cost = 0
        #Initial Deal
        for player in players:
            set_total, set1 = [], []  
            player_chips[player] = limit
            player_chips[player] -= blind
            card_str = ""
            for i in range(5):
                set1 = [suits[random.randint(1, 4)-1], cards[random.randint(1, 13)-1]]
                while set1 in all_sets:
                    set1 = [suits[random.randint(1, 4)-1], cards[random.randint(1, 13)-1]]
                all_sets.append(set1)
                set_total.append(set1)
            for thing in set_total:
                for other in thing:
                    card_str += str(display_cards[other])
            split_sets.append(set_total)
            deal_em = discord.Embed(title='You are Playing 5 card poker against {} | Here are your cards:'.format(players[counter1]), description=card_str)
            await player.send(embed=deal_em)
            players_cards[player] = set_total
        #Initial Betting Round
        one_cards, two_cards = split_sets[0], split_sets[1]
        ia, iv = 'Invalid Action', "You can't do that right now." 
        set_em = discord.Embed(title='.')
        act = ['bet', 'check', 'all in', 'fold', 'call', 'raise']
        player_str = ''
        player_str+=players[0].name
        player_str+=", "
        player_str+=players[1].name
        while game_stage<3 and fold_token==False:
            if game_stage == 0 or game_stage == 2:
                game_stage+=1
                bet_round = True
                if previous == 'all in':
                    break
                bet_msg = await ctx.send(embed=set_em)
                betting, actiont, previous, cost = True, False, 'none', blind
                while bet_round == True:
                    for player in players:
                        piv = 'none' #piv is used when bet or raised is called: it holds the value of the bet or raise
                        actiont = False #actiont needs to be reset every time since it would be left on true, which would evading the while loop
                        game_embed = discord.Embed(title='5 Card Poker | {}'.format(player_str), description = 'You are currently playing 5 card poker with a limit of {}'.format(limit))
                        game_embed.add_field(name='Current Player', value=player.name, inline=True)
                        game_embed.add_field(name='Pool Value', value=pool, inline=True)
                        game_embed.add_field(name='Your Chips', value=player_chips[player], inline=True)
                        game_embed.add_field(name='Previous Action', value=previous, inline=True)
                        if betting == True:
                            game_embed.add_field(name='Minimal Bet Cost', value=blind, inline=True)
                        else:
                            game_embed.add_field(name='Call Cost', value=cost, inline=True)
                        await bet_msg.edit(embed=game_embed)
                        while actiont == False:
                            error_em = discord.Embed(title='An Error Occured')
                            def check(m):
                                if m.author == player and m.channel == channel:
                                    return 'play'
                            try:
                                msg = await self.client.wait_for('message', timeout=60.0, check=check)
                                msg1 = msg.content
                            except asyncio.TimeoutError:
                                msg1 = "fold"
                            actiont = True
                            if msg1[:3]=='bet':
                                piv, msg1 = int(msg1[4:]), 'bet' 
                            try:
                                if msg1[:5]=='raise':
                                    piv, msg1 = int(msg1[6:]), 'raise'
                            except:
                                pass
                            if msg1 not in act and isinstance(msg1[-1], int)==False:
                                actiont = False
                                continue
                            else: 
                                if betting==True and msg1 in act[4:]: #checks for invalid actions while betting is true, won't catch raise
                                    error_em.add_field(name=ia, value=iv)
                                    await ctx.send(embed=error_em)
                                    actiont = False
                                    continue
                                elif betting==False:
                                    if msg1[:3]==act[0] or msg1=='check': #checks for invalid actions while betting is false
                                        error_em.add_field(name=ia, value=iv)
                                        await ctx.send(embed=error_em)
                                        actiont = False
                                        continue
                            #checks if the values that come with the command is valid
                            if msg1 == act[0] or msg1 == act[4] or msg1 == act[5]: #bet, call, raises
                                if msg1==act[0] and piv<blind:
                                    error_em.add_field(name='The Bet is Too Small', value='The minimal bet is 20 chips.')
                                    await ctx.send(embed=error_em)
                                    actiont = False
                                elif msg1==act[0] or msg1==act[5]: #checks bets and raises to see if the player has enough money
                                    if player_chips[player]<piv:
                                        error_em.add_field(name='Insufficient Chips', value='You do not have enough chips to do this.')
                                        await ctx.send(embed=error_em)
                                        actiont = False
                                elif msg1==act[4] and cost>player_chips[player]: #checks calls by comparing variable "cost"
                                        error_em.add_field(name='Insufficient Chips', value='You do not have enough chips to do this.')
                                        await ctx.send(embed=error_em)
                                        actiont = False
                        if msg1==act[0]: #bet
                            previous, cost, betting = 'bet', piv, False
                            pool +=piv
                            player_chips[player]-=piv
                        elif msg1==act[1]: #check
                            if previous == "check":
                                bet_round = False
                                break
                            previous='check'
                        elif msg1==act[2]: #all in
                            betting = False
                            pool += player_chips[player]
                            player_chips[player], cost = 0, -1
                            if previous == 'all in':
                                bet_round = False
                                break
                            previous='all in'
                        elif msg1==act[3]: #fold
                            fold_token, bet_round, fold_player = True, False, player
                            break
                        elif msg1==act[4]: #call
                            bet_round=False
                            if previous == 'all in':
                                pool+=player_chips[player]
                                player_chips[player] = 0
                                break
                            pool+=cost
                            player_chips[player]-=cost
                            previous='call'
                            break
                        elif msg1==act[5]: #raise
                            pool+=piv
                            player_chips[player]-=piv
                            cost=piv
                        else:
                            await ctx.send('something went wrong; check the code that interprets the action, this shoudlnt happen')
                            return
                if game_stage==1:
                    bet_close_em = discord.Embed(title='Betting Has Finished', description="The pot is worth {}! You will now discard unpreferable cards. Type the position of the card in your hand you want to discard with 1 space inbetween each position. You may discard up to 3 cards, or type 'stay' if you perfer to keep your hand. Your first card is at position 1, and you last card is at position 5".format(pool))
                    hot_fix1 = await ctx.send(embed=bet_close_em)
                else:
                    bet_close_em = discord.Embed(title='Betting Has Finished Again', description="The pot is worth {}! You will now compare hands, and the player with the highest hand will win the entire pot.".format(pool))
                await bet_msg.delete()
                    
                #swap card swap system ##############
                if game_stage == 1:
                    game_stage+=1
                    while one_swap  == False or two_swap == False:
                        error_em = discord.Embed(title='An Error Occured')
                        def check(m):
                            if m.author == player1 or m.author == player2:
                                return 'play'
                        try:
                            msg = await self.client.wait_for('message', timeout=60.0, check=check)
                            msg1, swapl = msg.content, []
                        except asyncio.TimeoutError:
                            fold_token = True
                            break
                        if msg == False:
                            continue
                        
                        if msg1 != 'stay' and msg1 != 'Stay':    
                            try:
                                swapl = msg1.split(' ')
                                if len(swapl)>3:
                                    await ctx.send('')
                                for i in range(len(swapl)):
                                    swapl[i] = (int(swapl[i]))-1
                                    if swapl[i]>5 or swapl[i]<0:
                                        await ctx.send('') #this will cause an error (to trigger except) since you can't send a empty msg
                            except:
                                error_em.add_field(name='Incorrect Input Format', value='please use the format of <card position>, <card position>, etc... to swap cards. You can only exchange a maximum of 3 cards.')
                                await ctx.send(embed=error_em)
                                continue
                            
                        if msg.author == player1:
                            if one_swap == True:
                                continue
                            swapu, cp, one_swap = player1, one_cards, True
                        else:
                            if two_swap == True:
                                continue
                            swapu, cp, two_swap = player2, two_cards, True
                        if len(swapl) !=0:
                            bet_close_em.add_field(name='{} Card Swap'.format(swapu.name), value='swapped {} card(s)'.format(len(swapl)))
                        else:
                            bet_close_em.add_field(name='{} Card Swap'.format(swapu.name), value="stayed.")
                            await hot_fix1.edit(embed=bet_close_em) #repeated code, could probably be more effecient
                            continue
                        await hot_fix1.edit(embed=bet_close_em)
                        for i in range(len(swapl)):
                            all_sets.remove(cp[swapl[i]])
                            new_card = [suits[random.randint(1, 4)-1], cards[random.randint(1, 13)-1]]
                            while new_card in all_sets:
                                new_card = [suits[random.randint(1, 4)-1], cards[random.randint(1, 13)-1]]
                            all_sets.append(new_card)
                            cp[swapl[i]] = new_card
                        card_str = ""
                        for card in cp:
                            for thing in card:
                                card_str+=display_cards[thing]
                        new_em = discord.Embed(title='Swapped Cards | Here are your new cards:', description=card_str)
                        await swapu.send(embed=new_em)

        if fold_token == True:
            winner = players[0]
            players.remove(fold_player)
            fold_em = discord.Embed(title='5 Card Poker | Game End by Fold', description="{} has folded, and {} wins the entire pot ({} chips). ".format(fold_player.name, winner.name, pool))
            await ctx.send(embed=fold_em)
            users[str(winner.id)]["chips"]+=pool #adds winnings to winner
            users[str(winner.id)]["chips"]+=player_chips[winner]
            users[str(winner.id)]["chips"]+=player_chips[fold_player]
        else:
            showdown_cards = []
            combinations = ['high card', 'one pair', 'two pair', '3 of a kind', 'straight', 'flush', 'full house', '4 of a kind', 'straight flush', 'royal flush']
            winner = 'none1'
            for player in players:
                count, suit_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0]
                hand_value, pair_counter, three_counter, kicker, fbk = 0, 0, 0, 0, 0
                hand = players_cards[player]
                flush_counter, straight_counter = False, False 
                suit_convert = {
                    ':diamonds:': 0,
                    ':clubs:': 1,
                    ':hearts:': 2,
                    ':spades:': 3
                }
                for i in range(5):
                    count[hand[i][1]-2]+=1
                    suit_count[suit_convert[hand[i][0]]]+=1
                try:
                    for i in range(13):
                        if count[i]>=2: #this is actually needed for the system that checks subsequent pairs or trio to work.
                            if count[i] == 2: 
                                pair_counter +=1
                                if three_counter == 0:
                                    kicker = i+2
                            elif count[i] == 3:
                                kicker = i+2
                                three_counter +=1
                            elif count[i] == 4: #four of a kind detection and proccesssing needs work
                                hand_value = 7
                                kicker = i+2
                                break
                            for j in range(12-i): #checks for subsequent pairs and trios, the 12 might have to be 13
                                if count[j+i+1]==2:
                                    pair_counter+=1
                                    if three_counter==0 and (i+j+2)>kicker:
                                        kicker = i+j+2
                                    elif three_counter == 1:
                                        fbk = i+j+2 #fbk is used as a tiebreaker in full house ties
                                    await ctx.send('')
                                elif count[j+i]==3:
                                    three_counter+=1
                                    if pair_counter == 1:
                                        fbk = kicker #if it becomes a full house, the pair value gets pushed to fbk
                                    kicker = i+j+2 #the 3 of a kind value takes the place of kicker
                                    await ctx.send('')
                except:
                    pass
                if pair_counter == 0 and three_counter == 0:
                    for i in range(4):
                        if suit_count[i]==5:
                            flush_counter = True
                            for i in range(5):
                                if hand[i][1]>kicker:
                                    kicker = hand[i][1]
                            break
                    for i in range(5):
                        try:
                            if count[i]==1 and count[i+1]==1 and count[i+2]==1 and count[i+3]==1 and count[i+4]==1:
                                straight_counter == True
                                break
                        except:
                            break
                    if straight_counter == True and flush_counter == True: #test for royal flush
                        if count[8]==1 and count[9]==1 and count[10]==1 and count[11]==1 and count[12]==1:
                            hand_value = 9
                        else:
                            hand_value = 8
                    elif flush_counter == True:
                        hand_value = 5
                    elif straight_counter == True:
                        hand_value = 4
                else:
                    if three_counter == 1:
                        if pair_counter==1:
                            hand_value = 6
                        else:
                            hand_value = 3
                    else:
                        if pair_counter == 1:
                            hand_value = 1
                        elif pair_counter == 2:
                            hand_value = 2
                if hand_value == 0: #assigns kicker the highest card if the hand is high card
                    for i in range(len(count)):
                        if count[i]>0 and (i+2)>kicker:
                            kicker = i+2
                showdown_cards.append([hand_value, kicker, fbk])
            for i in range(3):
                if i == 2 and three_counter == 0:
                    break
                if showdown_cards[0][i]>showdown_cards[1][i]:
                    winner = players[0]
                    break
                elif showdown_cards[0][0]<showdown_cards[1][i]:
                    winner = players[1]
                    break
                else:
                    pass
            if winner == 'none1':
                final_em = discord.Embed(title="5 Card Poker Results | It's a Draw!", description='Both players have the same hand and highest card. hand: {}, highest card: {}'.format(combinations[showdown_cards[0][0]], display_cards[showdown_cards[0][1]]))
            else:
                if winner == players[0]:
                    final_em = discord.Embed(title="5 Card Poker Results | {} Wins! ".format(winner.name), description='hand: {}, highest card: {}'.format(combinations[showdown_cards[0][0]], display_cards[showdown_cards[0][1]]))
                elif winner == players[1]:
                    final_em = discord.Embed(title="5 Card Poker Results | {} Wins! ".format(winner.name), description='hand: {}, highest card: {}'.format(combinations[showdown_cards[1][0]], display_cards[showdown_cards[1][1]]))
                wstr = ""
                for card in players_cards[winner]:
                    for individual in card:
                        wstr+=display_cards[individual]
                final_em.add_field(name='Cards', value=wstr)
            await ctx.send(embed=final_em)
            player_chips[winner]+=pool
            users[str(players[0].id)]["chips"]+=player_chips[players[0]]
            users[str(players[1].id)]["chips"]+=player_chips[players[1]]
        with open('bot_cogs/casinovault.json', "w") as f: 
            json.dump(users, f)
                        



    @commands.command()
    async def squares(self, ctx, bet=0):
        if bet<10:
            await ctx.send(embed=discord.Embed(title="Bet Error", description='The minimum bet is 10 tokens. use ";squares <bet>" '))
            return
        await self.open_account(ctx.author) 
        users = await self.get_account_data()
        users[str(ctx.author.id)]["chips"]-=bet

        initial_cols, initial_rows, moves = {random.randint(0, 9) for _ in range(5)}, {random.randint(0, 9) for _ in range(5)}, 0
        gameI, rcount, best = [[":white_large_square:" for _ in range(10)] for __ in range(10)], 0, len(initial_cols)+len(initial_rows)
        for thing in initial_cols:
            for i in range(10):
                if gameI[i][thing] == ":white_large_square:": gameI[i][thing], rcount = ":red_square:", rcount+1
                else: gameI[i][thing], rcount = ":white_large_square:", rcount-1
        for thing in initial_rows:
            for i in range(10):
                if gameI[thing][i] == ":white_large_square:": gameI[thing][i], rcount = ":red_square:", rcount+1
                else: gameI[thing][i], rcount = ":white_large_square:", rcount-1

        display, letter_display = ":zero: :one: :two: :three: :four: :five: :six: :seven: :eight: :nine: \n", [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:", ":regional_indicator_j:"]
        for f, t in enumerate(gameI): display+=str(" ".join(t))+letter_display[f]+"\n"
        game_msg = await ctx.send(embed=discord.Embed(title="{}'s Squares Game".format((str(ctx.author))[:-5]), description=display+"\nType the corrposponding letter/number with the row/column to change it. Use ;square_rules to find out more."))
        valid_row_moves, valid_col_moves = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9}
        row_reverse_convert = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J"}
        def check(m):
            if m.author == ctx.author and (m.content in valid_row_moves or m.content in valid_col_moves): return 'move'

        while True:
            if moves == best:
                optimal_path = ""
                for c in initial_cols: optimal_path+=str(c)+", "
                for r in initial_rows: optimal_path+=row_reverse_convert[r]+", "
                await game_msg.edit(embed=discord.Embed(title="You Lost!", description="You took more moves than the optimal solution. An optimal solution was: {}".format(optimal_path[:-2])))
                with open('bot_cogs/casinovault.json', "w") as f:
                    json.dump(users, f)
                return
            moves+=1
            try:
                msg = await self.client.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                game_msg.edit(embed=discord.Embed(title="You Ran Out of Time!", description="You have at most 30 seconds to make each move."))
                with open('bot_cogs/casinovault.json', "w") as f:
                    json.dump(users, f)
            
            if msg.content in valid_row_moves:
                for i in range(10):
                    if gameI[i][int(msg.content)] == ":white_large_square:": gameI[i][int(msg.content)], rcount = ":red_square:", rcount+1
                    else: gameI[i][int(msg.content)], rcount = ":white_large_square:", rcount-1
            else:
                for i in range(10):
                    if gameI[valid_col_moves[msg.content]][i] == ":white_large_square:": gameI[valid_col_moves[msg.content]][i], rcount = ":red_square:", rcount+1
                    else: gameI[valid_col_moves[msg.content]][i], rcount = ":white_large_square:", rcount-1
            
            display = ":zero: :one: :two: :three: :four: :five: :six: :seven: :eight: :nine: \n"
            for f, t in enumerate(gameI): display+=str(" ".join(t))+letter_display[f]+"\n"
            await game_msg.edit(embed=discord.Embed(title="{}'s Squares Game".format((str(ctx.author))[:-2]), description=display))

            if rcount == 0:
                await game_msg.edit(embed=discord.Embed(title="Squares Cleared!", description="You solved this squares game in {} moves. You won {}!".format(best, int(int(bet)*1.5))))
                users[str(ctx.author.id)]["chips"]+=int(int(bet)*1.5)
                with open('bot_cogs/casinovault.json', "w") as f:
                    json.dump(users, f)
                return


async def setup(client):
    await client.add_cog(gamble(client))
