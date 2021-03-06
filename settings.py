import proxies


# address of proxy server
# always in this format: {'connection type', 'proxy type://address:port'}
# proxies = {'https': 'socks5://user:password@ip:port'}
proxies = proxies.proxies

# additional url for each market - constant
# format: markets_url = 'https://www.marathonbet.com/en/markets.htm'
markets_url = 'https://www.marathonbet.com/en/markets.htm'

# main market addresses
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/England/Premier+League/'
# to indicate multiple markets separator (, ) - comma and space
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/England/Premier+League/, https://www.marathonbet.com/en/betting/Football/Russia/Premier+League/'

# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Ice+Hockey/Internationals/World+Championship/2019/Top+Division/Slovakia/'

# England. Premier League
TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/England/Premier+League/'

# England. Championship
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/popular/Football/England/Championship/'

# Clubs. International. Champions League
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/popular/Football/Clubs.+International/UEFA+Champions+League'

# Russia. Premier League
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/Russia/Premier+League/'

# Spain. Primera Division
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/Spain/Primera+Division/'

# Italy. Serie A
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/Italy/Serie+A/'

# Germany. Bundesliga
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/Germany/Bundesliga/'

# France. Ligue 1
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/France/Ligue+1/'

# FIFA World Cup
# TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/Internationals/FIFA+World+Cup/2018/Final+Tournament/Russia/'

###TOURNAMENTS_URL = 'https://www.marathonbet.com/en/betting/Football/Internationals/FIFA+World+Cup/2018/Final+Tournament/Russia/Group+Stage/Egypt+vs+Uruguay+-+6173501/'

teams = {'Manchester City': 'MCI',
         'Liverpool': 'LIV',
         'Chelsea': 'CHE',
         'Tottenham Hotspur': 'TOT',
         'Arsenal': 'ARS',
         'Manchester United': 'MUN',
         'Wolverhampton Wanderers': 'WOL',
         'Everton': 'EVE',
         'Leicester City': 'LEI',
         'West Ham United': 'WHU',
         'Watford': 'WAT',
         'Crystal Palace': 'CRY',
         'Newcastle United': 'NEW',
         'Bournemouth': 'BOU',
         'Burnley': 'BUR',
         'Southampton': 'SOU',
         'Brighton & Hove Albion': 'BHA',
         'Norwich City': 'NOR',
         'Sheffield United': 'SHU',
         'Aston Villa': 'AVL',
         'Cardiff City': 'CAR',
         'Fulham': 'FUL',
         'Huddersfield Town': 'HUD',
         'Leeds United': 'LEE',
         'West Bromwich Albion': 'WBA',
         'Derby County': 'DER',
         'Middlesbrough': 'MID',
         'Bristol City': 'BRC',
         'Nottingham Forest': 'NOF',
         'Swansea City': 'SWA',
         'Sheffield Wednesday': 'SHW',
         'Hull City': 'HUL',
         'Brentford': 'BRE',
         'Preston North End': 'PRE',
         'Blackburn Rovers': 'BLA',
         'Stoke City': 'STK',
         'Birmingham City': 'BIR',
         'Wigan Athletic': 'WIG',
         'Queens Park Rangers': 'QPR',
         'Reading': 'REA',
         'Millwall': 'MIL',
         'Luton Town': 'LUT',
         'Barnsley': 'BAR',
         'Charlton Athletic': 'CHA', }
