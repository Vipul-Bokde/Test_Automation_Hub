class ElementsLengthChanges(object):

    def __init__(self, locator, length):
        self.locator = locator
        self.length = length

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        element_count = len(elements)
        if element_count >= self.length:
            return elements
        else:
            return False


class ElementHasAnyText(object):

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        element_text = element.text
        text_size = len(element_text)
        if text_size > 3:
            return element
        else:
            return False
