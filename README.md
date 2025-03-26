## setup
folder should be in 
HMS
  -hms
  -staff
  -manage.py
  -db.sqlite
 in the above structure to run the server use 
 'python manager.py runserver' 
make sure you have installed the django

AIM 
Hospital Management System (HMS) project is to develop an integrated digital platform 
that streamlines the administrative and clinical operations of healthcare facilities. The system 
is designed to enhance efficiency by automating processes such as patient registration, 
appointment scheduling, billing, and medical record management.  
Additionally, the HMS incorporates a secure, role-based login system that directs users, 
including doctors and administrative staff, to customized dashboards, ensuring that each user 
has access to the tools and information relevant to their specific responsibilities. By centralizing 
and securing patient data, the HMS aims to improve the quality of care, reduce errors, and 
support better decision-making within the hospital environment. 

## explaination
Traditional HMS solutions often require patients to navigate cumbersome processes, 
including account creation and login, which can hinder access to healthcare services. Our HMS 
addresses these challenges by allowing patients to book appointments directly from the index 
page without the need for an account. Users can simply provide and informed decision-making. 
their name, phone number, and email address, and select the desired doctors. Ensuring that 
patients are matched with the most appropriate healthcare provider for their needs. Upon 
booking an appointment, patients can view the status of their bookings using their name and 
phone number. This approach simplifies the user experience and broadens access to healthcare 
services. Additionally, each patient is assigned a unique patient ID in the format 
YYYYMMDD***, where *** is a three-digit auto-incremented number. This unique identifier 
aids in efficient patient tracking and record-keeping, streamlining hospital operations.  
The Hospital Management System (HMS) incorporates a sophisticated user role-based login 
system, designed to streamline hospital operations and enhance security. During the account 
creation process, users are assigned to specific groups within Django based on their selected 
roles. This system ensures that users are directed to the appropriate dashboard tailored to their 
responsibilities, providing a more efficient and focused user experience.  
The system supports two primary user roles: doctors and registers. Doctors are responsible for 
confirming appointments booked via the index page and providing patient care, while registers 
manage patient admissions and discharges. This separation of roles ensures that healthcare 
professionals can focus on their specific responsibilities, thereby enhancing operational 
efficiency and reducing administrative burdens.  
A notable feature of the HMS is the automated PDF generation of billing documents at the time 
of patient discharge. This functionality not only ensures accurate and timely billing but also 
provides patients with a clear and detailed record of their medical expenses, which can be used 
for insurance claims or personal records. 
The HMS also includes an admin role with comprehensive system oversight capabilities. The 
admin can add users, manage data, and utilize visualization tools powered by Chart.js for real
time monitoring of patient admissions, discharges, and other critical metrics. This feature-rich 
admin dashboard, built using Django's administration interface, allows for effective resource 
management The primary objectives of this project are to develop a user-friendly, secure, and 
efficient system that enhances patient care and optimizes hospital management processes. 
Fig 3.1:- System Architecture 
At first, the user can directly access the index page to book an appointment without any need 
for logging in. On the index page, the user can select the doctor they wish to book an 
appointment with based on their medical needs. The user must fill out the appointment form 
with all necessary details. Additionally, users can check their appointment status and view 
patient details directly  
The staff login system differentiates roles based on their functions: Register, Doctor, and 
Admin. Each role has specific responsibilities and access within the system. 
• Admin: The Admin has the main authority over the system. They can add new doctors, 
registers, and departments. Admins are responsible for enrolling doctors into specific 
departments and solving customer queries through administration panel. They manage the 
entire portal, ensuring smooth operation and coordination between different roles. 
• Register: The Register is responsible for taking patient admissions, acting as a cashier for 
bill payments, and discharging patients. They ensure that all administrative tasks related to 
patient management are handled efficiently. 
• Doctor: Doctors manage appointments booked by users, accessing their dashboard to view 
new appointments, manage existing ones, and update appointment statuses from pending 
to confirmed or canceled. Once confirmed, appointments can be further updated to 
completed. Additionally, doctors are responsible for creating new bills for admitted 
patients, ensuring that medical and financial records are accurately maintained. 
The website is adaptive and secure, ensuring easy access for all users, staff, and administrators. 
The system securely stores all data in the database, providing a reliable and efficient hospital 
management system. 
