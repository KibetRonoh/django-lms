from django import template
import math
register = template.Library()


@register.simple_tag
def discount_calculation(price, discount):
    if discount is None or discount is 0:
        return price
    sellingprice = price
    sellingprice = price - (price * (discount / 100))
    return float(format(sellingprice, '.2f'))


@register.simple_tag
def calc_five_star(five_review_count, total_review_count):
    five_review_percentage = (five_review_count / total_review_count) * 100
    return math.ceil(five_review_percentage)


@register.simple_tag
def calc_hours(time_duration):
    hours = (time_duration / 60)
    return math.floor(hours)


@register.simple_tag
def calc_minutes(time_duration):
    minutes = (time_duration % 60)
    return minutes


@register.simple_tag
def calc_four_star(four_review_count, total_review_count):
    four_review_percentage = (four_review_count / total_review_count) * 100
    return math.ceil(four_review_percentage)


@register.simple_tag
def calc_three_star(three_review_count, total_review_count):
    three_review_percentage = (three_review_count / total_review_count) * 100
    return math.ceil(three_review_percentage)


@register.simple_tag
def calc_two_star(two_review_count, total_review_count):
    two_review_percentage = (two_review_count / total_review_count) * 100
    return math.ceil(two_review_percentage)


@register.simple_tag
def calc_one_star(one_review_count, total_review_count):
    one_review_percentage = (one_review_count / total_review_count) * 100
    return math.ceil(one_review_percentage)


@register.simple_tag
def calc_average_rating(one_review_count, two_review_count, three_review_count, four_review_count,
                        five_review_count, total_review_count):
    overall_review = ((one_review_count*1) + (two_review_count*2) + (three_review_count*3)
                     + (four_review_count*4) + (five_review_count*5)) / total_review_count
    return round(overall_review, 2)