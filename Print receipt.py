def main():
    """
    the main game function
    calls all the other functions
    prints to invoice to console and writes to a file called 'invoice.txt'
    :return: None
    """

    # call the draw table function
    table = ['Product code', 'Product Name', 'Quantity', 'Supplier', 'cost']
    table = draw_table(table)

    # Make a divider
    divider = '+' + '-' * 14 + '+' + '-' * 18 + '+' + '-' * 8 + '+' + '-' * 16 + '+' + '-' * 10 + '+'

    # open a file to be written on
    file = open('orders.txt', 'w')

    # make the headders
    print(divider)
    file.write(divider+'\n')
    print(table)
    print(divider)
    file.write(table+'\n')
    file.write(divider+'\n')

    # call the make line function to print the lines after the headers
    order = make_line()

    # print each line on list with proper string formatting
    for i in order:
        line = "|{:^13s} |{:^18.17}|{:8d}|{:>15} | ${:7.2f} |".format(*i)
        print(line)
        file.write(line+'\n')
    print(divider)
    file.write(divider+'\n')

    # compute the toal cost of the order
    total_cost = 0
    for i in order:
        price = i[4]
        total_cost += price
    line = "|{:^13s} |{:>8}{:>10.2f}|".format('Total Coast', '$', total_cost)
    print(line)
    file.write(line+'\n')
    bottom_divider = '+' + '-' * 14 + '+' + '-' * 18 + '+'
    print(bottom_divider)
    file.write(bottom_divider+'\n')

    # get the highest cost list and print and wrtie
    high_cost = get_highest_cost()
    for i in high_cost:
        line = 'Highest cost: {1:<11s}{0:>12s} [{2:.2f}]'.format(*i)
        print(line)
        file.write(line+'\n')


def products():
    """
    takes in the products file
    deletes the newline character
    formats the list into a dict
    :return: product dictionary
    """
    # open file to be read
    f1 = open('products.txt', 'r')

    # convert product data to list
    product_data = [line.strip('\n') for line in f1]

    # convert list into a dictionary separtaed by ';'
    product_dictionary = dict((line.strip().split(';') for line in product_data))

    return product_dictionary


def suppliers():
    """
    takes in the supplier file
    deletes the newline character
    creates a list separated by ';'
    deletes the address of the supplier since it is not needed
    formats the phone number to look like a national phone number (no country codes)
    no need for supplier dictionaary
    :return: supplier list
    """
    # open file to be read
    f2 = open('suppliers.txt', 'r')

    # strips new line character
    suppliers_data = [line.strip('\n') for line in f2]

    # creates a list of lists separated by ';'
    suppliers_data = [line.split(';')for line in suppliers_data]

    # delete the address from the list because it is never needed
    for i in suppliers_data:
        del i[2]

    # format the phone numbers
    for i in suppliers_data:
        i[0] = '('+i[0][:3]+')'+' '+i[0][3:6]+' '+i[0][6:]

    return suppliers_data


def availability():
    """
    takes in the availability data file
    strips the newline character
    creates a list separated by a ','
    run a for loop to check if any two lines have the same product code
    check the prices and delete the more expesnive supplier
    :return: availability data dict
    """
    # open file to be read
    f3 = open('availability.txt', 'r')

    # convert availability data to list separated by ','
    availability_data = [line.strip('\n') for line in f3]
    availability_data = [line.split(',') for line in availability_data]

    # take the list to check if two products are being offered by two different suppliers and take the cheaper supplier
    availability_dictionary = {}
    for sublist in availability_data:
        if sublist[0] not in availability_dictionary.keys():
            availability_dictionary.update({sublist[0]: [sublist[1], sublist[2]]})
        else:
            if sublist[2] < availability_dictionary[sublist[0]][1]:
                availability_dictionary[sublist[0]][1] = sublist[2]
    return availability_dictionary


def on_shelves():
    """
    take in the on shelve data text file
    strip the new line character
    convert list to dictionary separated by '#' to be used later
    :return: on_shelves_data_dictionary
    """
    # open file to be read
    f4 = open('onshelves.txt', 'r')

    # convert on shelves data to list
    on_shelves_data = [line.strip('\n') for line in f4]

    # convert the list into a dictionary
    on_shelves_data_dictionary = dict((line.strip().split('#') for line in on_shelves_data))

    return on_shelves_data_dictionary


def draw_table(table):
    """
    docstrings
    use string formating to make table headers
    ensure they are aligned
    :return: table_headers
    """
    table_headers = "| {:^13s}|{:<18s}|{:<8s}|{:<16s}|{:<9s} |".format(*table)
    return table_headers


def make_line():
    """
    takes in 3 of 4 dictionaries and makes a line
    appends each line in order to a list
    formats the phone numbers
    sort the list by phone number in ascending order
    :return: order list
    """
    # create a list of lists each element in the sublist being each line in the invoice
    availability_dictionary = availability()
    product_dictionary = products()
    on_shelves_data_dictionary=on_shelves()
    order = []
    for k, v in on_shelves_data_dictionary.items():
        for key, value in product_dictionary.items():
            for key1, value1 in availability_dictionary.items():
                if int(v) < 20 and k == key == key1:
                    quantity = 50 - int(v)
                    price = float(value1[1])
                    cost = int(quantity) * price
                    if quantity > 40:
                        value = '*' + value
                    else:
                        value = ' ' + value
                    order.append([key, value, quantity, value1[0], cost])  # append line to list

    # format the phone numbers
    for i in order:
        i[3] = '(' + i[3][:3] + ')' + ' ' + i[3][3:6] + ' ' + i[3][6:]

    # sort the list by the supplier phone number
    order.sort(key=lambda x: x[3], reverse=True)
    return order


def get_highest_cost():
    """
    finds and creates a list of the highest cost
    makes a list of lines to be printed
    :return: high cost list
    """
    order = make_line()
    supplier_list = suppliers()

    # find the highest cost
    cost_list = []
    for i in order:
        cost_list.append([i[4]])

    # create a list of the highest costs
    highest_cost = [i for i in cost_list if i == max(cost_list)]

    # append the cost to the supplier list
    for i in order:
        for k in supplier_list:
            for x in highest_cost:
                if i[3] == k[0] and i[4] == x[0]:
                    k.append(i[4])

    # sort the supplier list
    supplier_list.sort(key=lambda x: (x[1]))

    # format the lines to be printed
    high_cost_list = []
    for i in supplier_list:
        if len(i) > 2:
            high_cost_list.append(i)
    return high_cost_list


main()
