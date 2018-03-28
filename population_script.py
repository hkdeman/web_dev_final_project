import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','web_dev_final_project.settings')
from tqdm import tqdm
import json
import django
django.setup()
from unevu.models import *

import unevu.utils as util

if __name__ == "__main__":
	file = open("assets/glasgow_university_subject_data.json", "r")
	glasgow_courses = json.loads(file.read())

	file = open("assets/glasgow_university_teacher_data.json", "r")
	glasgow_teachers = json.loads(file.read())

	file = open("assets/top_50_university_data.json","r")
	universities = json.loads(file.read())

	for university in tqdm(universities,desc="Adding Universities"):
		util.add_uni(university, "United Kingdom", "Quisque nec mi id nisi interdum cursus vitae quis velit. \
				 Duis id dapibus lorem, a ornare lacus. Phasellus congue tellus est. \
				 Duis egestas faucibus orci, facilisis suscipit sapien ornare id.  \
				 Nulla sed enim in leo pharetra scelerisque ac id nibh. \
				 Cras finibus orci sem, quis euismod augue tincidunt a. Nam malesuada faucibus luctus. ",
				 55.3781, -3.4)

	gla = util.add_uni("University of Glasgow", "Glasgow, Scotland",
				"The University of Glasgow is the sixth oldest university in the English-speaking world \
				and one of Scotland's four ancient universities. It was founded in 1451. \
				Along with the University of Glasgow, the University was part of the \
				Scottish Enlightenment during the 18th century. It is currently a member \
				of Universitas 21 and the Russell Group.",
				55.87212109999999,-4.288200500000016)
	edi = util.add_uni("University of Edinburgh", "Edinburgh, Scotland",
				"The University of Edinburgh is the fourth oldest university in the English-speaking world \
				and one of Scotland's four ancient universities. It was founded in 1451. \
				Along with the University of Edinburgh, the University was part of the \
				Scottish Enlightenment during the 18th century. It is currently a member \
				of Universitas 21, the international network of research universities and the Russell Group.",
				55.9473899,-3.187194)

	sta = util.add_uni("University of St Andrews", "St Andrews, Scotland",
				"The University of St Andrews is the most overrated in the English-speaking world \
				and the oldest of Scotland's four ancient universities. It was founded in 1412.",
				56.3417,-2.7928)



	test_user1 = util.add_user("mrtest1", "mrtest1@test.com", "Test1", "User")
	test_user2 = util.add_user("mrtest2", "mrtest2@test.com", "Test2", "User")
	test_user3 = util.add_user("clum", "mrtest3@test.com", "Calum", "Mackay")
	util.add_uni_review(gla, test_user1, "Very good uni. Fandabbydozy!", 4)
	util.add_uni_review(gla, test_user2, "Too many people roll up their trousers", 2)
	util.add_uni_review(gla, test_user3, "I live for HIVE", 5)
	util.add_uni_review(edi, test_user1, "Everyone is boring", 1)
	util.add_uni_review(sta, test_user1, "The people here actually clap at the end of lectures. ", 2)


				 
	for school in glasgow_courses:
		curr_school = util.add_school(school["title"], gla)
		print("Processing " + school["title"] + " courses")
		for course in tqdm(school.get("subjects", [])):
			util.add_course(course["title"], curr_school, "https://www.gla.ac.uk"+course["url"], course["description"] )

		print("Processing " + school["title"] + " teachers")
		for teacher in tqdm(glasgow_teachers.get(school.get("title", []), [])):
			contact = teacher.get("contact", {})
			if contact==None:
				contact = {}
			util.add_teacher(teacher["name"], curr_school, 
				contact.get("email", ""),contact.get("mobile", ""),
				teacher.get("image", ""))
		print()

	#Sets test review for Economics 1A
	course = Course.objects.get(id = 1)
	teacher = Teacher.objects.get(name = "Harless, Dr Patrick")
	util.set_convener_to_course(course,teacher)

	test_user = util.add_user("mrtest0", "mrtest0@test.com", "Test", "User")
	util.add_course_review(course, test_user, "Very good course. Fandabbydozy!", 4)
