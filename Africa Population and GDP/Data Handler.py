import csv
    

id_i = 0
year_i = 1
country_i = 2
continent_i = 3
population_i = 4
gdp_i = 5


def readfile(filename: str):
    file = open(filename, 'r')
    reader = csv.reader(file, delimiter=',')
    
    # get the rows of the file
    rows = []
    for row in reader:
        rows.append(row)

    return rows


def readContinents(rows):
    # read the continets
    continents = []
    for row in rows:
        if row[continent_i] not in continents:
            continents.append(row[continent_i])
    # write the continents to a file
    file = open('Continents.txt', 'w')
    file.write('Africa has the following continents: ')
    for continent in continents:
        file.write(continent + ', ')
    file.close()
    return continents


def readCountries(rows, continents):
    # read the continent-country pair
    continent_country = {}
    for continent in continents:
        continent_country[continent] = []
        for row in rows:
            if row[continent_i] == continent:
                if row[country_i] not in continent_country[continent]:
                    continent_country[continent].append(row[country_i])
    # write the continent-country pair to a txt file
    # Note: the newline is needed as Windows automatically adds a newline by \r\r\n
    file = open('Continent-to-Country.txt', 'w')
    for continent in continents:
        file.write(continent + ' has the following countries:')
        for country in continent_country[continent]:
            file.write(country + ', ')
        file.write('\n')
    file.close()
    # write the continent-country pair to a csv file
    file = open('Continent-to-Country.csv', 'w', newline="")
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['question', 'answer'])
    for continent in continents:
        writer.writerow(["What countries are in " + continent + "?", continent_country[continent]])
    file.close()
    return continent_country


def readCountryPopulation(rows):
    # read the country-and-year-population pair
    country_year_population = {}
    for row in rows:
        if row[country_i] not in country_year_population:
            country_year_population[row[country_i]] = {}
        if row[year_i] not in country_year_population[row[country_i]]:
            country_year_population[row[country_i]][row[year_i]] = row[population_i]
    # write the country-and-year-population pair to a txt file
    file = open('Country-to-Year-Population.txt', 'w')
    for country in country_year_population:
        file.write("The population for " + country + " changes as the following: ")
        for year in country_year_population[country]:
            file.write(year + ': ' + country_year_population[country][year] + '; ')
        file.write('\n')
    file.close()
    # write the country-and-year-population pair to a csv file
    file = open('Country-to-Year-Population.csv', 'w', newline="")
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['question', 'answer'])
    for country in country_year_population:
        year_population = ''
        for year in country_year_population[country]:
            year_population += "In year " + year + ", the population is " + country_year_population[country][year] + '; '
        writer.writerow(["How is the population chaning in " + country + "?", year_population])
    file.close()
    return country_year_population


def main():
    rows = readfile('Data_Africa.csv')

    # remove the header
    rows.pop(0)

    # read the continets
    continents = readContinents(rows)

    # read the continent-country pair
    continent_country = readCountries(rows, continents)

    # read the country-and-year-population pair
    country_year_population = readCountryPopulation(rows)

if __name__ == '__main__':
    main()
     
