# Content

* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)

## General info
<details>
<summary>see <b>general info</b></summary>
  This project is an API built with <b>Django REST framework</b> that allows authenticated users to upload images via HTTP request.
</details>

## Technologies
<details>
<summary>see <b>technologies</b></summary>
<ul>
  <li>Django</li>
  <li>Django REST Framework</li>
  <li>Docker Compose</li>
  <li>PostgreSQL</li>
  <li>Celery</li>
  <li>Redis</li>
</ul>
</details>

## Setup
<details>
<summary>see <b>setup</b></summary>

To run this project on your machine it is required to have installed previously Docker Compose on your computer. For further information, see [documentation](https://docs.docker.com/compose/install/ "Install docker").

  1. [Clone](https://help.github.com/articles/cloning-a-repository/) the repository on your machine.
  2. Create a .env file at the base of the project repository, in which you'll have to set the variables below.
       <details>
       <summary>see .env file variables</summary>
        SECRET_KEY<br>
        DEBUG<br>
        ALLOWED_HOSTS<br>
        DATABASE_NAME<br>
        DATABASE_USER<br>
        DATABASE_PASSWORD<br>
        DATABASE_HOST<br>
        </details>
  3. At the base of the project repository run the command: `docker compose up --build -d`
  4. Open the link to the web app in your web browser: http://0.0.0.0/
</details>

## More detailed information about modules
<details>
<summary>see <b>info about modules</b></summary>
  <ul>
    <li>The app allows authenticated user to upload images via HTTP requests.</li>
    <li>Authentication is done through token.</li>
    <li>Depending on user type (basic, premium or enterprise), different versions of the image they uploaded will be generated.</li>
    <li>There is a fourth user type available, custom, which profile can be set by admins from django admin UI.</li>
    <li>The image versions can be generated as binary image and/or thumbnails, different sizes of latter are generated based on user profile.</li>
    <li>Users have access to the list of all images they uploaded with the link to display it, along with the links to the different versions of the image they can access.</li>
    <li>Users who have access to binary image have to set an expiration time during which the image can be accessed, once this time is up, the image won't be available anymore.</li>
  </ul>
</details>
