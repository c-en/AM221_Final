library(rgdal)

# Citation: https://cran.r-project.org/doc/contrib/intro-spatial-rl.pdf
# Read in shape file (from https://docs.digital.mass.gov/dataset/massgis-data-community-boundaries-towns-survey-points)
setwd("~/Applied Math 221/Final Project/AM221_Final-master/Maps") # Change this to match your computer
require(rgdal)
shape <- readOGR(dsn=".",layer = "TOWNSSURVEY_POLY") # Make sure this file is in your working directory
plot(shape)

# Color town of Sheffield red (as a test). Should be near bottom left corner
sheffield <- shape$TOWN == "SHEFFIELD"
plot(shape[sheffield,], col = "red", add = TRUE) # add selected zones to map

# Towns in district 1
d1 <- c('ATTLEBORO',
        'EASTON',
        'BEVERLY',
        'DANVERS',
        'HAVERHILL',
        'LYNNFIELD',
        'MANCHESTER-BY-THE-SEA',
        'METHUEN',
        'GILL',
        'MONSON',
        'BELCHERTOWN',
        'PELHAM',
        'LINCOLN',
        'LITTLETON',
        'PEPPERELL',
        'SHERBORN',
        'SHIRLEY',
        'WALTHAM',
        'WESTFORD',
        'FRANKLIN',
        'HOLBROOK',
        'HINGHAM',
        'HULL',
        'ROCKLAND',
        'CHELSEA',
        'REVERE',
        'WINTHROP',
        'ASHBURNHAM',
        'BOYLSTON',
        'CHARLTON',
        'DOUGLAS',
        'EAST BROOKFIELD',
        'HOLDEN',
        'HUBBARDSTON',
        'MENDON',
        'MILLVILLE',
        'NORTH BROOKFIELD',
        'PAXTON',
        'SOUTHBRIDGE',
        'STERLING',
        'WARREN',
        'WEST BOYLSTON',
        'WESTMINSTER')

# District 2
d2 <- c('FALL RIVER',
        'FREETOWN',
        'AMESBURY',
        'ESSEX',
        'GROVELAND',
        'MARBLEHEAD',
        'MERRIMAC',
        'NAHANT',
        'NEWBURYPORT',
        'NORTH ANDOVER',
        'ROWLEY',
        'SALISBURY',
        'WEST NEWBURY',
        'ERVING',
        'PALMER',
        'WARE',
        'ARLINGTON',
        'BELMONT',
        'BILLERICA',
        'CHELMSFORD',
        'DRACUT',
        'DUNSTABLE',
        'TEWKSBURY',
        'TYNGSBOROUGH',
        'WOBURN',
        'BRAINTREE',
        'FOXBOROUGH',
        'MEDWAY',
        'RANDOLPH',
        'WESTWOOD',
        'LAKEVILLE',
        'MIDDLEBOROUGH',
        'NORWELL',
        'PEMBROKE',
        'PLYMPTON',
        'SCITUATE',
        'WEST BRIDGEWATER',
        'WHITMAN',
        'HARDWICK',
        'UPTON')

# District 3
d3 <- c('FALMOUTH',
        'ACUSHNET',
        'RAYNHAM',
        'REHOBOTH',
        'EDGARTOWN',
        'OAK BLUFFS',
        'BOXFORD',
        'HAMILTON',
        'SALEM',
        'SAUGUS',
        'WENHAM',
        'ACTON',
        'ASHLAND',
        'BEDFORD',
        'CONCORD',
        'HOLLISTON',
        'HUDSON',
        'LEXINGTON',
        'MALDEN',
        'MELROSE',
        'NATICK',
        'STONEHAM',
        'WILMINGTON',
        'WINCHESTER',
        'AVON',
        'COHASSET',
        'DEDHAM',
        'DOVER',
        'NORWOOD',
        'SHARON',
        'WELLESLEY',
        'WRENTHAM',
        'BRIDGEWATER',
        'HANOVER',
        'KINGSTON',
        'MARION',
        'MATTAPOISETT',
        'PLYMOUTH')

# District 4
d4 <- c('LYNN',
        'EVERETT',
        'NANTUCKET',
        'BROOKLINE',
        'CANTON',
        'MEDFIELD',
        'MILLIS',
        'MILTON',
        'NEEDHAM',
        'NORFOLK',
        'PLAINVILLE',
        'QUINCY',
        'STOUGHTON',
        'WALPOLE',
        'WEYMOUTH',
        'ABINGTON',
        'BROCKTON',
        'CARVER',
        'DUXBURY',
        'EAST BRIDGEWATER',
        'HALIFAX',
        'HANSON',
        'MARSHFIELD',
        'ROCHESTER',
        'WAREHAM')

# District 5
d5 <- c('BARNSTABLE',
        'BOURNE',
        'BREWSTER',
        'CHATHAM',
        'DENNIS',
        'EASTHAM',
        'HARWICH',
        'MASHPEE',
        'ORLEANS',
        'PROVINCETOWN',
        'SANDWICH',
        'TRURO',
        'WELLFLEET',
        'YARMOUTH',
        'FAIRHAVEN',
        'NEW BEDFORD',
        'NORTON',
        'SOMERSET',
        'SWANSEA',
        'TAUNTON',
        'WESTPORT',
        'AQUINNAH',
        'CHILMARK',
        'TISBURY',
        'WEST TISBURY',
        'GLOUCESTER',
        'ROCKPORT',
        'SWAMPSCOTT',
        'TOPSFIELD',
        'BURLINGTON',
        'CARLISLE',
        'MAYNARD',
        'MEDFORD',
        'NORTH READING',
        'READING',
        'SUDBURY',
        'WAKEFIELD',
        'WATERTOWN',
        'WAYLAND',
        'WESTON',
        'BELLINGHAM')

# District 6
d6 <- c('ANDOVER',
        'GEORGETOWN',
        'IPSWICH',
        'LAWRENCE',
        'MIDDLETON',
        'NEWBURY',
        'PEABODY',
        'GREENFIELD',
        'WARWICK',
        'WHATELY',
        'CAMBRIDGE',
        'FRAMINGHAM',
        'HOPKINTON',
        'LOWELL',
        'MARLBOROUGH',
        'NEWTON',
        'SOMERVILLE',
        'TOWNSEND',
        'BERLIN',
        'SOUTHBOROUGH')

# District 7
d7 <- c('ADAMS',
        'ALFORD',
        'BECKET',
        'DALTON',
        'EGREMONT',
        'FLORIDA',
        'GREAT BARRINGTON',
        'HANCOCK',
        'HINSDALE',
        'LANESBOROUGH',
        'LEE',
        'MOUNT WASHINGTON',
        'NEW ASHFORD',
        'NEW MARLBOROUGH',
        'NORTH ADAMS',
        'PITTSFIELD',
        'RICHMOND',
        'SAVOY',
        'SHEFFIELD',
        'STOCKBRIDGE',
        'TYRINGHAM',
        'WASHINGTON',
        'WEST STOCKBRIDGE',
        'WILLIAMSTOWN',
        'WINDSOR',
        'ASHFIELD',
        'BERNARDSTON',
        'BUCKLAND',
        'CHARLEMONT',
        'HAWLEY',
        'HEATH',
        'LEVERETT',
        'SUNDERLAND',
        'BLANDFORD',
        'CHESTER',
        'CHICOPEE',
        'GRANVILLE',
        'HAMPDEN',
        'HOLLAND',
        'LONGMEADOW',
        'LUDLOW',
        'MONTGOMERY',
        'RUSSELL',
        'SOUTHWICK',
        'SPRINGFIELD',
        'TOLLAND',
        'WEST SPRINGFIELD',
        'AMHERST',
        'CUMMINGTON',
        'EASTHAMPTON',
        'HADLEY',
        'PLAINFIELD',
        'SOUTH HADLEY',
        'SOUTHAMPTON',
        'AYER',
        'PHILLIPSTON',
        'PRINCETON',
        'WEST BROOKFIELD',
        'WINCHENDON',
        'WORCESTER')

# District 8
d8 <- c('CHESHIRE',
        'CLARKSBURG',
        'LENOX',
        'MONTEREY',
        'OTIS',
        'PERU',
        'SANDISFIELD',
        'COLRAIN',
        'CONWAY',
        'DEERFIELD',
        'LEYDEN',
        'MONROE',
        'MONTAGUE',
        'NEW SALEM',
        'NORTHFIELD',
        'ORANGE',
        'ROWE',
        'SHELBURNE',
        'SHUTESBURY',
        'WENDELL',
        'AGAWAM',
        'EAST LONGMEADOW',
        'HOLYOKE',
        'WALES',
        'WESTFIELD',
        'WILBRAHAM',
        'CHESTERFIELD',
        'GOSHEN',
        'GRANBY',
        'HATFIELD',
        'HUNTINGTON',
        'MIDDLEFIELD',
        'NORTHAMPTON',
        'WESTHAMPTON',
        'WILLIAMSBURG',
        'WORTHINGTON',
        'ASHBY',
        'BOXBOROUGH',
        'GROTON',
        'STOW',
        'ATHOL',
        'AUBURN',
        'BARRE',
        'BLACKSTONE',
        'BOLTON',
        'BROOKFIELD',
        'CLINTON',
        'DUDLEY',
        'FITCHBURG',
        'GARDNER',
        'GRAFTON',
        'HARVARD',
        'HOPEDALE',
        'LANCASTER',
        'LEICESTER',
        'LEOMINSTER',
        'LUNENBURG',
        'MILFORD',
        'MILLBURY',
        'NEW BRAINTREE',
        'NORTHBOROUGH',
        'NORTHBRIDGE',
        'OAKHAM',
        'OXFORD',
        'PETERSHAM',
        'ROYALSTON',
        'RUTLAND',
        'SHREWSBURY',
        'SPENCER',
        'STURBRIDGE',
        'SUTTON',
        'TEMPLETON',
        'UXBRIDGE',
        'WEBSTER',
        'WESTBOROUGH')

# District 9
d9 <- c('BERKLEY',
        'DARTMOUTH',
        'DIGHTON',
        'MANSFIELD',
        'NORTH ATTLEBOROUGH',
        'SEEKONK',
        'GOSNOLD',
        'BRIMFIELD',
        'BOSTON')

# Color towns in each district a different color
for (i in 1:length(d1))
{
  current_town <- shape$TOWN == d1[i]
  plot(shape[current_town,], col = "blue", add = TRUE) # Color towns of district 1 blue
}

for (i in 1:length(d2))
{
  current_town <- shape$TOWN == d2[i]
  plot(shape[current_town,], col = "green", add = TRUE) 
}

for (i in 1:length(d3))
{
  current_town <- shape$TOWN == d3[i]
  plot(shape[current_town,], col = "red", add = TRUE)
}

for (i in 1:length(d4))
{
  current_town <- shape$TOWN == d4[i]
  plot(shape[current_town,], col = "yellow", add = TRUE) 
}

for (i in 1:length(d5))
{
  current_town <- shape$TOWN == d5[i]
  plot(shape[current_town,], col = "pink", add = TRUE) 
}

for (i in 1:length(d6))
{
  current_town <- shape$TOWN == d6[i]
  plot(shape[current_town,], col = "orange", add = TRUE) 
}

for (i in 1:length(d7))
{
  current_town <- shape$TOWN == d7[i]
  plot(shape[current_town,], col = "white", add = TRUE) 
}

for (i in 1:length(d8))
{
  current_town <- shape$TOWN == d8[i]
  plot(shape[current_town,], col = "purple", add = TRUE) 
}

for (i in 1:length(d9))
{
  current_town <- shape$TOWN == d9[i]
  plot(shape[current_town,], col = "turquoise", add = TRUE)
}

# Print legend for colors
# https://www.math.ucla.edu/~anderson/rw1001/library/base/html/legend.html
# https://stackoverflow.com/questions/14883238/adding-simple-legend-to-plot-in-r
legend('bottomleft',legend=c('District 1','District 2','District 3','District 4','District 5',
                         'District 6','District 7','District 8','District 9'), 
       fill=c('blue','green','red','yellow',
      'pink','orange','white','purple','turquoise'), ncol=3, bty = "o",cex=0.8)

