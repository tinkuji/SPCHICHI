import re

def lexical_analyzer(input_string):
    # Regular expressions to match numbers, identifiers, and keywords
    number_pattern = r'\d+'
    identifier_pattern = r'[a-zA-Z_]\w*'
    keyword_pattern = r'\b(if|else|while|for|break|continue|return)\b'
    
    tokens = []
    
    while input_string:
        # Remove leading whitespace
        input_string = input_string.lstrip()
        
        # Match number pattern
        match = re.match(number_pattern, input_string)
        if match:
            number = match.group()
            tokens.append(('NUMBER', number))
            input_string = input_string[len(number):]
            continue
        
        # Match identifier pattern
        match = re.match(identifier_pattern, input_string)
        if match:
            identifier = match.group()
            
            # Check if it's a keyword
            if re.match(keyword_pattern, identifier):
                tokens.append(('KEYWORD', identifier))
            else:
                tokens.append(('IDENTIFIER', identifier))
                
            input_string = input_string[len(identifier):]
            continue
        
        # If no match is found, raise an error
        raise ValueError(f"Invalid token: {input_string}")
    
    return tokens


# Test the lexical analyzer
input_string = 'if x 42'
tokens = lexical_analyzer(input_string)

# Display the tokens
for token_type, token_value in tokens:
    print(f'Token Type: {token_type}, Token Value: {token_value}')