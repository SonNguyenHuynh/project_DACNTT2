
def generate_strings(self,characters):
    result = []

    def generate_helper(current_string, index):
        if index == len(characters):
            if current_string:  # Only append non-empty strings
                result.append(current_string)
            return
        # Include the character at the current index
        generate_helper(current_string + characters[index], index + 1)
        # Exclude the character at the current index
        generate_helper(current_string, index + 1)
    generate_helper('', 0)
    return result