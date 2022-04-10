from os import name
from discord.ext import commands
import discord, requests, json, random, asyncio, string, time

ip = requests.get('https://api.my-ip.io/ip').text

response = requests.post(
    "https://proxy.webshare.io/api/proxy/config/",
    json={"authorized_ips":[ip]},  
    headers={"Authorization": ""}
)

proxies = open('proxies.txt', 'r').read().splitlines()

bot = commands.Bot(command_prefix='.')
data = json.loads(open('database.json', 'r').read())

def getToken(blob):
    token = requests.post(
        'https://roblox-api.arkoselabs.com/fc/gt2/public_key/A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F',
        headers={
            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        },

        data={
            'public_key':'A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F',
            'rnd':f'0.{random.randint(1000,100000)}',
            'language':'en',
            'userbrowser':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
            'data[blob]':blob
        }
    )

    return token.json()['token']


def generate_username():
    while True:
        user = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + '_', k=random.randint(4, 7)))
        username = requests.get(f'https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={user}')
        if username.json()['message'] == "Username is valid":
            return user

@bot.command()
async def solve(ctx):
    proxy = random.choice(proxies)
    proxi = {'http':proxy, 'https':proxy}
    xtoken = requests.post(
                'https://auth.roblox.com/v1/signup',
                proxies = proxi
                ).headers[
                'x-csrf-token'
            ]
    captchaId = requests.post(
        'https://auth.roblox.com/v2/signup',

        proxies = proxi,

        json={'captchaId':'32', 'username':'james', 'captchaToken':'abc123'},

        headers={
            'x-csrf-token':xtoken,

            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',

            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/'

        }
    ).json()['failureDetails'][0]['fieldData'].split(',')
    token = getToken(captchaId[1])
    nwtoken = token.split('|')[0]
    custom_url = f"https://roblox-api.arkoselabs.com/fc/gc/?token={nwtoken}&r=us-west-2&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&ht=1&atp=2&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc&lurl=https%3A%2F%2Faudio-us-west-2.arkoselabs.com&surl=https%3A%2F%2Froblox-api.arkoselabs.com"
    await ctx.reply(f'<@{ctx.author.id}> when you finished please run the command `.done` to finish the task!')
    em = discord.Embed(title='Solve Captcha', description='Solve this captcha correctly for 1 robux!')
    em.add_field(name='Solve Captcha', value=f'[Click]({custom_url}) to open your captcha!')
    em.set_thumbnail(url='https://media.discordapp.net/attachments/909168538441351178/923440159586938970/Kobux.jpg?width=406&height=406')
    await ctx.reply(embed=em)
    def check(c):
        return c.content == '.done' and c.channel == ctx.channel and c.author == ctx.author
    
    await bot.wait_for('message', check=check)

    password = ''.join(random.choices(string.digits, k=10))
    username = generate_username()

    JSONSignup = {
        "agreementIds":[
            "848d8d8f-0e33-4176-bcd9-aa4e22ae7905",
            "54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3"
        ],

        "birthday":"21 Sep 2006",
        "captchaId":"",
        "captchaProvider":"PROVIDER_ARKOSE_LABS",
        "captchaToken":str(token),
        "context":"MultiverseSignupForm",
        "displayAvatarV2":False,
        "displayContextV2":False,
        "gender":2,
        "captchaId":captchaId[0],
        "isTosAgreementBoxChecked":True,
        "password":password,
        "username":username,
        "referralData":"null"
    }

    create = requests.post(
        'https://auth.roblox.com/v1/signup',

        data=JSONSignup,

        proxies=proxi,

        headers={
            'x-csrf-token':xtoken,

            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',

            'origin':'https://www.roblox.com',
            'referer':'https://www.roblox.com/'

        },

        
    )

    print(create.text)

    added = False
    if create.status_code == 200:
        anm1t = 1
        global data
        for acc in data:
            if acc['id'] == ctx.author.id:
                added = True
                data[data.index(acc)]['robux'] += anm1t
        
        if added == False:
            data.append({'id':ctx.author.id, 'robux':1})
            added = True

        cc = create.cookies['.ROBLOSECURITY']
        open('gen_cookies.txt', 'a').write(f'{username}:{password}:{cc}\n')
        open('database.json', 'w+').write(json.dumps(data))
        em = discord.Embed(title='Captcha Solved!', description=f'You have been added {anm1t} robux(s) for you to cashout on to your account, just type the command `.cashout <gamepass id> <amount>` to cashout your robux or do `.robux` to see the amount of robux you have!')
        em.set_thumbnail(url='https://media.discordapp.net/attachments/909168538441351178/923440159586938970/Kobux.jpg?width=406&height=406')
        await ctx.reply(embed=em)
        print('-> Solved captcha and generated cookie!')

@bot.command()
async def robux(ctx):
    for acc in data:
        if acc['id'] == ctx.author.id:
            robux = acc['robux']
            await ctx.reply(f'You have **{robux}** amount of robux!')
            return
    
    await ctx.reply(f'You have **0** amount of robux!')

@bot.command()
async def cashout(ctx, gamepassid, amount):
    for acc in data:
        if acc['id'] == ctx.author.id and acc['robux'] >= 15 and acc['robux'] >= int(amount):
            info = requests.get(
                f'https://api.roblox.com/marketplace/game-pass-product-info?gamePassId={gamepassid}',
                cookies={'.ROBLOSECURITY':'_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_0046AE06191C4DF96CE41C09F71CD4A36F2A3061AF196CE495D269BF4B986B36106EC6FE04D1F0BA0378F7B927607B90A8051F7CAD2349B1160BEECF5A9246F644B3C7793DB2C0D992C817181717B7BC54E3832AE839102C1CC353D96D1B7EC12C1C4C48C59CB1CA1CF886E269A38624A71A8A8AF95ABEB39BAACA3993A25170C3C1C2C905B295DAD438F729293EA28DD025004EAC0B5F5C94D9F7783578BD114944D905BB7B3B4C8E658A130DD801616BCF6BE0FF158F8FBB1CB8DFB418C10C1A68576BAC4093FDD31A07924C01BA7475E17A1A9702220BDFAC39EC7FC4B0FF8E5BB1ADAD8DD8C892AD51070BB2EE6F7936E4BCD7A725106E00DC698A6A83718A112F3571A7843E420CBD9BC4B0034FECE2AEBAE52E0A88D71031C08E9EF2D0EB0F73C9A387CB35FA5A3F25653A6046BF54AF7A815233512B02AFC7B76E4B3354B0CEFABD67029B4AB8B6D24227AD713F2E70B8'}
            ).json()

            my_robux = requests.get('https://api.roblox.com/currency/balance', cookies={'.ROBLOSECURITY':'_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_0046AE06191C4DF96CE41C09F71CD4A36F2A3061AF196CE495D269BF4B986B36106EC6FE04D1F0BA0378F7B927607B90A8051F7CAD2349B1160BEECF5A9246F644B3C7793DB2C0D992C817181717B7BC54E3832AE839102C1CC353D96D1B7EC12C1C4C48C59CB1CA1CF886E269A38624A71A8A8AF95ABEB39BAACA3993A25170C3C1C2C905B295DAD438F729293EA28DD025004EAC0B5F5C94D9F7783578BD114944D905BB7B3B4C8E658A130DD801616BCF6BE0FF158F8FBB1CB8DFB418C10C1A68576BAC4093FDD31A07924C01BA7475E17A1A9702220BDFAC39EC7FC4B0FF8E5BB1ADAD8DD8C892AD51070BB2EE6F7936E4BCD7A725106E00DC698A6A83718A112F3571A7843E420CBD9BC4B0034FECE2AEBAE52E0A88D71031C08E9EF2D0EB0F73C9A387CB35FA5A3F25653A6046BF54AF7A815233512B02AFC7B76E4B3354B0CEFABD67029B4AB8B6D24227AD713F2E70B8'}).json()['robux']

            if int(amount) == info['PriceInRobux'] and my_robux >= int(amount):
                buy = requests.post(
                    f'https://economy.roblox.com/v1/purchases/products/' + str(info['ProductId']),

                    json={
                        'expectedCurrency':1,
                        'expectedPrice':amount,
                        'expectedSellerId':info['Creator']['Id']
                    },

                    headers={
                        'x-csrf-token':requests.post('https://friends.roblox.com/v1/users/1/request-friendship', cookies={'.ROBLOSECURITY':'_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_0046AE06191C4DF96CE41C09F71CD4A36F2A3061AF196CE495D269BF4B986B36106EC6FE04D1F0BA0378F7B927607B90A8051F7CAD2349B1160BEECF5A9246F644B3C7793DB2C0D992C817181717B7BC54E3832AE839102C1CC353D96D1B7EC12C1C4C48C59CB1CA1CF886E269A38624A71A8A8AF95ABEB39BAACA3993A25170C3C1C2C905B295DAD438F729293EA28DD025004EAC0B5F5C94D9F7783578BD114944D905BB7B3B4C8E658A130DD801616BCF6BE0FF158F8FBB1CB8DFB418C10C1A68576BAC4093FDD31A07924C01BA7475E17A1A9702220BDFAC39EC7FC4B0FF8E5BB1ADAD8DD8C892AD51070BB2EE6F7936E4BCD7A725106E00DC698A6A83718A112F3571A7843E420CBD9BC4B0034FECE2AEBAE52E0A88D71031C08E9EF2D0EB0F73C9A387CB35FA5A3F25653A6046BF54AF7A815233512B02AFC7B76E4B3354B0CEFABD67029B4AB8B6D24227AD713F2E70B8'}).headers['x-csrf-token']
                    },
                    cookies={'.ROBLOSECURITY':'_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_0046AE06191C4DF96CE41C09F71CD4A36F2A3061AF196CE495D269BF4B986B36106EC6FE04D1F0BA0378F7B927607B90A8051F7CAD2349B1160BEECF5A9246F644B3C7793DB2C0D992C817181717B7BC54E3832AE839102C1CC353D96D1B7EC12C1C4C48C59CB1CA1CF886E269A38624A71A8A8AF95ABEB39BAACA3993A25170C3C1C2C905B295DAD438F729293EA28DD025004EAC0B5F5C94D9F7783578BD114944D905BB7B3B4C8E658A130DD801616BCF6BE0FF158F8FBB1CB8DFB418C10C1A68576BAC4093FDD31A07924C01BA7475E17A1A9702220BDFAC39EC7FC4B0FF8E5BB1ADAD8DD8C892AD51070BB2EE6F7936E4BCD7A725106E00DC698A6A83718A112F3571A7843E420CBD9BC4B0034FECE2AEBAE52E0A88D71031C08E9EF2D0EB0F73C9A387CB35FA5A3F25653A6046BF54AF7A815233512B02AFC7B76E4B3354B0CEFABD67029B4AB8B6D24227AD713F2E70B8'}
                )

                if buy.status_code == 200:
                    em = discord.Embed(title=f'Cashout success!', description=f'You have now gained your robux!')
                    em.set_thumbnail(url='https://media.discordapp.net/attachments/909168538441351178/923440159586938970/Kobux.jpg?width=406&height=406')
                    await ctx.reply(embed=em)
                    for acc in data:
                        if acc['id'] == ctx.author.id:
                            added = True
                            data[data.index(acc)]['robux'] -= int(amount)
                            open('database.json', 'w+').write(json.dumps(data))
                            break
                            
            else:
                await ctx.reply(f'We are currently having issues autherizing your request, we are probably out of stock or you are doing this wrong')

bot.run('')
