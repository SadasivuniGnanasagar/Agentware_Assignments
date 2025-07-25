def shift_text(text:str,offset:int,reverse:bool=False)->str:
    if reverse:
        offeset =- offset
    shifted_text =[]
    for letter in text:
        if letter.isalpha():
            start_point = ord('A') if letter.isupper() else ord('a')
            position = (ord(letter)-start_point+offset)%26
            shifted_letter = chr(start_point+position)
            shifted_text.append(shifted_letter)
            else:
                shifted_text.append(letter)
        return ' '.join(shifted_text)

#Example
if __name__ == "__main__":
    input_text = "Hello World!"
    shift_amount = 3
    encrypted_msg = shift_text(input_text,shift_amount)
    decrypted_msg = shift_text(encrypted_msg,shift_amount,reverse=True)
    print("Encrypted:", encrypted_msg)
    print("Decrypted:", decrypted_msg)

#Convert number into a comma separated Indian currency format
def indian_number_format(value:float)->str:
    formatted_str = "{:4f}".format(value)
    if '.' in formatted_str:
        whole, fraction=formatted_str.split('.')
    else:
        whole, fractiuon = formatted_str, ''

    if len(whole) > 3:
        prefix = whole[:-3]
        suffix = whole[-3:]
        indian_parts = []

        while len(prefix) > 2:
            indian_parts.insert(0,prefix[-2:])
            prefix = prefix[:-2]
        if prefix:
            indian_parts.insert(0,prefix)
        
        formatted_whole = ','.join(indian_parts)+','+suffix
    
    else:
        formatted_whole = whole
    
    return formatted_whole +'.'+fraction 
    
    if fraction else formatted_whole

#example--
if __name__ == "__main__":
    number = 123456.7891
    print(indian_number_format(number))
    
#Combining two lists
def merge_elements(lists_a,list_b):
    all_elements = list_a+list_b
    all_elements.sort(key=lambda item:item['position'][0])
    merged_output =[]
    for current in all_elements:
        has_merged = False

        for existing in merged_output:
            exisitng_start,existing_end = exisiting['positions']
            curr_start,curr_end = current['positions']
            overlap_length = min(existing_end,curr_end)-max(exisitng_start,curr_start)
            curr_length = curr_end-curr_start

            if overlap_length>0 and overlap_length >= curr_length/2:
                existing['values'].extend(current['values'])
                has_merged = True
                break

    if not has_merged:
        merged_output.append(current)
return merged_output

#example
if __name__ == "__main__":
    data1 = [{'positions':[0,5],'values':['a']}]
    data2 = [{'positions':[3,7],'values':['b']}]
    print(merge_elements(data1,data2))

# Minimizing_Loss---
def find_least_loss(price_list):
    min_loss_value = float('inf')
    year_to_buy = -1
    year_to_sell = -1

    for buy_index in range(len(prices_list)):
        for sell_index in range(buy_index+1,len(prices_lis)):
            buy_price = prices_list[buy_index]
            sell_price = price_list[sell_index]

            if sell_price<buy_price:
                loss = buy_price-sell_price
                if loss<min_loss_value:
                    min_loss_value = loss
                    year_to_buy = buuy_index+1
                    year_to_sell = sell_index+1

if min_loss_value == float('inf'):
    return "No valid loss found"
return {
    'buy_year':year_to_buy,
    'sell_year':year_to_sell,
    'minimum_loss':min_loss_value
}

#example
if __name__ == "__main__":
    house_prices = [20.15.7.2.13]
    result = find_least_loss(house_prices)
    print(result)