#!/usr/bin/python3
import os
import time
import math
import ipaddress

def subnetter(ip_address, cidr_notation, number_of_subnets_needed):
    """
    This function will take the ip address, cidr notation and the number of subnets, and will return a list of subnets
    """

    # Calculating the number of the bits you need to borrow from host, and the new CIDR notation
    bits_to_borrow = math.ceil(math.log2(number_of_subnets_needed))
    new_cidr_notation = bits_to_borrow + cidr_notation

    # Calculating the number of IP addresses in each subnet
    available_ips = 2 ** (32 - new_cidr_notation)

    # The Starting IP address as an integer
    starting_ip_int = int(ipaddress.IPv4Address(ip_address))

    # Creating a list of subnet info
    subnet_info = []
    for i in range(number_of_subnets_needed):
        # Calculating the network, starting, ending, and the broadcast address for each subnet
        network_address = starting_ip_int + (i * available_ips)
        start_ip = network_address + 1
        end_ip = network_address + available_ips - 2
        broadcast_address = network_address + available_ips - 1

        # Converting IP Addresses to strings
        network_address_str = str(ipaddress.IPv4Address(network_address))
        start_ip_str = str(ipaddress.IPv4Address(start_ip))
        end_ip_str = str(ipaddress.IPv4Address(end_ip))
        broadcast_address_str = str(ipaddress.IPv4Address(broadcast_address))

        # Appending the subnet information to the list
        subnet_info.append({
            "cidr_block": f"{network_address_str}/{new_cidr_notation}",
            "address_range": f"{start_ip_str} - {end_ip_str}",
            "broadcast_address": broadcast_address_str
        })

    for i, information in enumerate(subnet_info):
        print(f"Subnet-{i+1}:")
        print(f"\tCIDR Block: {information['cidr_block']}")
        print(f"\tAddress range: {information['address_range']}")
        print(f"\tBroadcast address: {information['broadcast_address']}")
        print("---------------------------------------------------")

# Inputs and Error handlers
while True:
    ip_address = str(input("Enter the IP address >> "))
    try:
        ipaddress.IPv4Address(ip_address)
        break
    except ValueError:
        print("\ninvalid IP address. please try again!")
        time.sleep(1.5)
        os.system("clear")

while True:
    try:
        cidr_notation = int(input("Enter the CIDR notation number >> "))
        if 1 <= cidr_notation <= 30:
            break
        else:
            print("\nCIDR notation must have a value between 1 - 30. Please try again")
            time.sleep(1.5)
            os.system("clear")

    except ValueError:
        print("\nInvalid input! please enter a number")
        time.sleep(1.5)
        os.system("clear")

while True:
    try:
        number_of_subnets_needed = int(input("Enter the number of subnets you desire to create >> "))
        if number_of_subnets_needed > 0:
            break
        else:
            print("\nNumber of subnets must be a positive number! Try again.")
            time.sleep(1.5)
            os.system("clear")

    except ValueError:
        print("Invalid output, Please enter a number!")
        time.sleep(1.5)
        os.system("clear")


print("\n******************** SUBNETTER ********************\n")
subnetter(ip_address, cidr_notation, number_of_subnets_needed)
