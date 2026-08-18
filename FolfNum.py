# A large number module built by QuantumFloof (@curiouslygenealogy) for a very beginner project. (6 hours in. :3); Will be updated every so often; Subject to performance optimizations, new functions, and changes.

# Import essential libraries. (I'm not sure If I need the decimal library anymore; I'll check.)
import math
from decimal import Decimal, DecimalTuple, getcontext

# Found this online, I don't need it anymore.
getcontext().Emax = 999999999999999999
getcontext().Emin = -999999999999999999

# Define the "FolfNum" class that is used for large numbers and split into sign, mantissa, exponent to signficantly preserve memory and bypass the 64-bit floating point integer limit.
class FolfNum:
    def __init__(self, sign: int, mantissa: float, exponent: int):
        self.sign = sign
        self.mantissa = mantissa
        self.exponent = exponent
        # Supports the helper function to display in the format of "-XeY" or "XeY"
    def __repr__(self):
        sign = "-" if self.sign else ""
        return f"{sign}{self.mantissa}e{self.exponent}"

# Extracts the mantissa. We don't really need this anymore as I can change the vital things it supports to make the code cleaner in the future; This commit, it may already be done.
def extractMantissa(m: tuple) -> float:
    mantissa = 0

    for digit in m:
        mantissa = (mantissa * 10) + digit

    return mantissa

# Normalizes FolfNum to properly "scale" exponents/mantissas.
def normalizeFolfNum(fN: FolfNum) -> FolfNum:
    if fN.mantissa == 0:
        return FolfNum(
            fN.sign,
            fN.mantissa,
            fN.exponent,
        )

    while abs(fN.mantissa) >= 10:
        fN.mantissa /= 10
        fN.exponent += 1

    while abs(fN.mantissa) < 1:
        fN.mantissa *= 10
        fN.exponent -= 1
    return fN
# Converts any datatype that holds "numerical information" from the perception of a human to a FolfNum
def convertDataTypeToFolfNum(dataType):
    if type(dataType) in (float, int, str):

        val_str = str(dataType).lower()

        sign = 1 if val_str.startswith("-") else 0
        if sign == 1:
            val_str = val_str[1:]

        if 'e' in val_str:
            base, exp = val_str.split('e')
            mantissa = float(base)
            exponent = int(exp)

        # Handles digit precision up to 15 places.
        elif '.' not in val_str and len(val_str) > 15:
            exponent = len(val_str) - 1
             # Neuter The folf :3
            mantissa = float(f'{val_str[0]}.{val_str[1:15]}')
        else:
            # Returns if it contains a "." and the length of the number is less than 15.
            mantissa = float(val_str)
            exponent = 0

        # Stores the datatype that was converted to FolfNum for usage.
        dataType: FolfNum = FolfNum(
                sign = sign,
                mantissa = mantissa,
                exponent = exponent
            )

        # Normalizes and returns the FolfNum.
        return normalizeFolfNum(dataType)


# Needs significant work or will break on current/future iterations.
def convertFolfNumToSpecifiedDataType(fN: FolfNum, dataTypeSpecified):
    if type(dataTypeSpecified) in (float, int):

        finalNum = fN.mantissa * (10 ** fN.exponent)

        if fN.sign == 1:
            finalNum *= -1

        return finalNum
    
    elif type(dataTypeSpecified) is str:
       
        finalNum = fN.mantissa * (10 ** fN.exponent)

        if fN.sign == 1:
            finalNum *= -1


        return f'{finalNum:.2e}'

# Converts FolfNums into a shortened suffix form resembling that of EternityNum (FoundForces) (Kinda/Mostly)
def shorten(fn1: FolfNum) -> str:
    firstSuffixes = ['K', 'M', 'B']
    secondSuffixes = ['', 'U', 'D', 'T', 'Qd', 'Qn', 'Sx', 'Sp', 'Oc', 'No']
    thirdSuffixes = ['', 'De', 'Vg', 'Tg', 'Qg', 'Qng', 'Sg', 'Spg', 'Og', 'Ng']
    fourthSuffixes = ['Ce', 'Du', 'Tr', 'Qa', 'Qi', 'Se', 'Si', 'Ot', 'Ni']
    fifthSuffixes = ['Mi', 'Mc', 'Na', 'Pi', 'Fm', 'At']

    # If the number's exponent is less than 3 or the suffix "K", return the float.
    if fn1.exponent < 3:
        return convertFolfNumToSpecifiedDataType(fn1, float)

    # Obtain the suffix index.
    suffixIndex = int(fn1.exponent // 3)

    # Combine suffixes so they can stack and be manipulated easily.
    stackingSuffixes = fourthSuffixes + fifthSuffixes

    # Get the remainder to scale the mantissa.
    exponentRemainder = int(fn1.exponent % 3)
    # Scale the mantissa.
    scaledMantissa = fn1.mantissa * (10 ** exponentRemainder)
    # Check the correct "sign".
    sign_Str = '-' if fn1.sign == 1 else ""

    #
    if 1 <= suffixIndex <= 3:
        return f'{sign_Str}{scaledMantissa:.2f}{firstSuffixes[suffixIndex - 1]}'

    # Subtract the suffix index to account for the suffix table's indexes starting at 0.
    N = suffixIndex - 1

    # Continuing to split the "number" mathematically/arithmetically.
    ones = N % 10
    tens = (N // 10) % 10
    hundreds = N // 100

    # Building the number's "suffix"
    suffix = secondSuffixes[ones] + thirdSuffixes[tens]

    # if the "hundreds" that defines the absolute "highest point" is greater than 0, than continue the operations to stack the suffixes on the fourth & fifth suffix tables.
    if hundreds > 0:
        # initiate the "hundreds_suffix" str as empty.
        hundreds_suffix = ""
        # iterate through fourth suffixes. (may need to change to stackingSuffixes.)
        for i in range(len(stackingSuffixes)):
          if (hundreds >> i) & 1:
            hundreds_suffix += stackingSuffixes[i]
        suffix += hundreds_suffix

    # Return the number + it's suffix in the format "-XeY" or "XeY" to two decimal precision points.
    return f'{sign_Str}{scaledMantissa:.2f}{suffix}'


# Adds FolfNums
def add(fN1: FolfNum, fN2: FolfNum):

    # If a is greater than b.. than set the correct "values" to each "bigger" and "smaller" variables.
    if fN1.exponent >= fN2.exponent:
        bigger = fN1
        smaller = fN2
    # if a is less than b.. than set the correct "values" to each "bigger" and "smaller" variables.
    elif fN1.exponent < fN2.exponent:
        bigger = fN2
        smaller = fN1

    # Retrieve and store the differences of the bigger and smaller exponents.
    difference =  bigger.exponent - smaller.exponent

    # smaller mantissa alignment/"correction".
    smallerMantissa = smaller.mantissa * (10 ** -difference)
    # combine the mantissa's of the smaller and "bigger".
    finalMantissa = bigger.mantissa + smallerMantissa

    # Retrive and store the bigger exponent.
    finalExponent = max(fN1.exponent, fN2.exponent)

    # weird ass logical handling. will be fixed in the next commit most likely.
    sign = max(fN1.sign, fN2.sign)

    # return the normalized FolfNum to it's class for further modifications.
    return normalizeFolfNum(FolfNum(
        sign = sign,
        mantissa = finalMantissa,
        exponent = finalExponent,
    ))

# Subtract a number from another number. (a - b)
def sub(fN1: FolfNum, fN2: FolfNum):

    m1 = fN1.mantissa if fN1.sign == 0 else -fN1.mantissa
    m2 = fN2.mantissa if fN2.sign == 0 else -fN2.mantissa

    finalExponent = max(fN1.exponent, fN2.exponent)

       # Check if number is bigger than the other one by a substantial amount; If it is, then practically do nothing.
    if abs(fN1.exponent - fN2.exponent) > 15:
        return normalizeFolfNum(FolfNum(fN1.sign, fN1.mantissa, fN1.exponent)) if fN1.exponent > fN2.exponent else normalizeFolfNum(FolfNum(fN2.sign, -fN2.mantissa if fN2.sign==0 else fN2.mantissa, fN2.exponent))

    m1_aligned = m1 * (10 ** (fN1.exponent - finalExponent))
    m2_aligned = m2 * (10 ** (fN2.exponent - finalExponent))

    # Retrive and store the bigger exponent.
    finalMantissa = m1_aligned - m2_aligned

    if finalMantissa < 0:
        finalSign = 1
        finalMantissa = abs(finalMantissa)
    else:
        finalSign = 0

    # return the normalized FolfNum to it's class for further modifications.
    return normalizeFolfNum(FolfNum(
        sign = finalSign,
        mantissa = finalMantissa,
        exponent = finalExponent,
    ))


# Multiply a number by another number.
def mul(fN1: FolfNum, fN2: FolfNum):
    # Quite simple.

    # Multiply the mantissa to replicate the style of multiplying the numbers in mathematics.. and add the exponents.
    newMantissa = fN1.mantissa * fN2.mantissa
    newExponent = fN1.exponent + fN2.exponent

    # Check whether negative or positive.. As multiplying anything but by it's own status of negative or positive in multiplication to check if it's negative or positive.
    if fN1 != fN2:
        sign = 1
    else:
        sign = 0

    return normalizeFolfNum(FolfNum(
        sign = sign,
        mantissa = newMantissa,
        exponent = newExponent,
    ))

# Divide a number by another number
def div(fN1: FolfNum, fN2: FolfNum):
    # The inverse of multiplication.

    # Handle division by 0.
    if fN2.mantissa == 0:
        raise ValueError("Division by 0 error. Have fun being sucked up by a black hole.")

    # Very simple shit; If you understand the previous parts of this module compentently.. this will be no where near hard to understand.

    newMantissa = fN1.mantissa / fN2.mantissa
    newExponent = fN1.exponent - fN2.exponent

    if fN1 != fN2:
        sign = 1
    else:
        sign = 0

    return normalizeFolfNum(FolfNum(
        sign = sign,
        mantissa = newMantissa,
        exponent = newExponent,
    ))

# Checks if a number is greater than another number.
def gt(a: FolfNum, b: FolfNum) -> bool:
    if a.sign != b.sign:
        return a.sign == 0

    if a.sign == 0:
        if a.exponent != b.exponent:
            return a.exponent > b.exponent
        else:
            return a.mantissa > b.mantissa
        
    else:
        if a.exponent != b.exponent:
            return a.exponent < b.exponent
        else:
            return a.mantissa < b.mantissa

# Checks if a number is less than another number.
def lt(a: FolfNum, b: FolfNum) -> bool:
    gt(b, a)
        

# Test print statement.

num1 = convertDataTypeToFolfNum('1e3')
num2 = convertDataTypeToFolfNum('1e3') 

print(f'n3: {gt(num1, num2)}')