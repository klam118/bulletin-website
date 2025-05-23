import requests
from bs4 import BeautifulSoup
import json
import re

def extract_course_codes(text):
    """
    Extracts valid course codes (e.g., 'AMS 113', 'MAT 125') from a given text.
    """
    course_code_pattern = r'\b[A-Z]{2,4} \d{3}[A-Z]?\b'
    return re.findall(course_code_pattern, text)

def extract_data(course):
    course_info = {}
    block = [child.strip() for child in course.stripped_strings]

    # Extract course title
    course_title = block[0].replace('\u00a0', ' ')
    course_info['title'] = course_title

    # Extract course description
    course_description = block[1]
    course_info['description'] = course_description

    # Find and capture prerequisite text (even if it's across multiple lines)
    prerequisite_text = ""
    # beginning P can be upper case or lower case and account for potential s at the end of line
    prereq_pattern = re.compile(r'(?i)^p(?:r)?erequisite[s]?:')

    capture = False

    for line in block:
        if prereq_pattern.search(line):
            prerequisite_text = line  # Start capturing when a matching line is found
            capture = True
        elif capture and line and "Anti-requisite" not in line:
            prerequisite_text += " " + line  # Continue capturing subsequent lines
        else:
            capture = False  # Stop capturing when a new section is reached

    # Extract course codes **only from the prerequisite text**
    course_info["prerequisite"] = extract_course_codes(prerequisite_text)

    # Append course data
    course_data.append(course_info)

if __name__ == "__main__":
    majors = []
    with open('majors.json', 'r') as f:
        majors = json.load(f)

    for major in majors:
        url = f"https://www.stonybrook.edu/sb/bulletin/current/courses/{major}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all(class_="course")
        course_data = []

        # Loop through each course element
        for course in courses:
            extract_data(course)

        # Save data as JSON file
        with open(f'{major}.json', 'w') as f:
            json.dump(course_data, f, indent=4)


        ###### DEBUGGING DONT DELETE ######
        # major = "ams"
        # url = f"https://www.stonybrook.edu/sb/bulletin/current/courses/{major}/"
        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, 'html.parser')
        # courses = soup.find_all(class_="course")
        # course_data = []

        # # Loop through each course element
        # for course in courses:
        #     extract_data(course)

        # # Save data as JSON file
        # with open(f'{major}.json', 'w') as f:
        #     json.dump(course_data, f, indent=4)