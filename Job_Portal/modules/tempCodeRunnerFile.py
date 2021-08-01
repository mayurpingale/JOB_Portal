
in_first = set(fixedStatus)
in_second = set(status)

in_second_but_not_in_first = in_second - in_first

result = fixedStatus + list(in_second_but_not_in_first)