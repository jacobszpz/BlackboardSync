# Universities

> [!NOTE]
> Even though here only referred to as "university", you can file a
> request to suport any type of Blackboard Learn instance,
> including colleges, schools, etc.

[Jump to supported universities](#supported-universities)


## Adding support for your university

In order to support your university, some information is first needed.


### Necessary data to add support

#### Basic Information

- **University name** (e.g. *University of Central Lancashire*).
- **Short name** or abbreviation (e.g. *UCLan*) if one exists.
- **Link to Blackboard portal** (e.g. *https://portal.uclan.ac.uk*).
- **Landing URL** after successfully logging in
  (e.g. *https://portal.uclan.ac.uk/ultra*).

#### Automatic Detection

In order to allow users to complete their setup process faster,
there is a built-in university detection system based on the
Internet Service Provider.
Note that this only works if you are currently connected to the
university network.
Fortunately, finding the required information is easy:

a. Visit our [automated checker][rdap-check] and note the result down.

b. **If the automated checker is not working**, follow these steps:

1. Find out your ip by visiting https://api.ipify.org/.
2. Visit https://rdap.org and enter your ip.
3. Note down the content of `Network Name`, `Country`, and `Remarks`.
   You can use `Ctrl+F` to find these fields.
4. Let me also know that the checker is down.


> There are [other fields](#advanced-fields) you can collect but
  I strongly suggest you skip these


### Ready to contribute?

Please create an issue using [the following form][support-issue].
You will need a GitHub account to do so.

> [!IMPORTANT]
> Once you create the issue, a Pull Request will be generated
> automatically for you. Creating one on your own is discouraged.

If you don't have an account with GitHub, and would rather not
create one, feel free to reach me at request@bbsync.app instead.

Finally, you can instead post your request in our official
[`Matrix` space](https://matrix.to/#/#blackboardsync:matrix.org).

In every case, your contribution will be credited to your username and
in the case of GitHub, you will be made author of the final commit.

If this is not something you'd like, please let me know.


## Supported Universities

### Europe

#### United Kingdom

###### England

- University of Central Lancashire
- University of Westminster
- University of Reading
- University of East Anglia
- Durham University
- University of Salford
- University of Leicester
- Imperial College London
- University of Bristol
- University of Sheffield
- Buckinghamshire New University
- University of Northampton
- University of Bedfordshire
- Leeds Beckett University
- Sheffield Hallam University
- University of the West of England
- Northumbria University
- Edge Hill University
- University of Lincoln
- University of Derby
- University of Manchester
- University of York

###### Scotland

- University of Aberdeen
- The University of Edinburgh
- Glasgow Caledonian University

###### Northern Ireland

- Ulster University

###### Wales

- University of South Wales
- Cardiff University

#### Rest of Europe

- Universidad Europea Madrid
- Universidad de Alcala
- Trinity College Dublin
- University of Antwerp
- Universidade do Minho
- Hanze University of Applied Sciences
- Centro Universitario de Tecnología y Arte Digital
- OBS Business School
- Universidad Pablo de Olavide
- Università Bocconi

### North America

###### United States of America

- University of Arkansas
- The George Washington University
- Alaska Pacific University
- Youngstown State University
- Ohio University
- Post University
- The University of Alabama
- Concordia University Wisconsin & Ann Arbor
- Sam Houston State University
- University of Connecticut
- Schoolcraft College
- Texas Tech University
- University of Texas at Dallas
- University of Evansville
- Mid-State Technical College
- University of Maryland, Baltimore County
- Syracuse University
- University of Illinois Chicago
- San Jacinto College

###### Canada

- Georgian College
- Seneca Polytechnic
- Humber College Institute of Technology and Advanced Learning

### South America

- Universidad Tecnologica ECOTEC
- Universidad de Palermo
- Universidad Tecnologica del Salvador
- Universidad Ana G. Mendez

###### Mexico

- Universidad del Valle de Mexico
- Universidad Regional del Sureste

### Asia

- Princess Nourah Bint Abdulrahman University
- The Chinese University of Hong Kong
- The Chinese University of Hong Kong, Shenzhen
- Hong Kong Community College
- Shiv Nadar University

### Australia

- Torrens University
- Holmes Institute
- University of Western Australia
- Griffith University
- Curtin University
- Western Sydney University

###### New Zealand

- University of Otago

### Africa

- University of Pretoria
- École Supérieure Privée d'Ingénierie et de Technologies

If any information here seems wrong, please let me know in the issues.



------



## Footnotes



#### Advanced fields

- **Valid Blackboard data sources**

This is a tricky one because it can potentially help filter out dummy courses and other folders with no user content.

However, its usage may vary per institution, ultimately is not necessary, and if set incorrectly it may cause other users to not see any course at all.

You are fine without it and it is suggested to be skipped. If you have more information about how these are set internally, please let me know.

> To know this, you'll need to login to blackboard on a browser, and then visit the
> endpoint "/learn/api/public/v1/users/me/courses" on your university blackboard page.
> For instance, this might be: "https://portal.uclan.ac.uk/learn/api/public/v1/users/me/courses".
>
> Once on this page, you will see the list of courses you are registered for. Entries are of this form:

> ```json
> {
>   "id":"...",
>   "userId":"...",
>   "courseId":"...",
>   "dataSourceId":"_21_1",
>   "created":"...",
>   "modified":"...",
>   "availability":{"available":"Yes"},
>   "courseRoleId":"Student",
>   "lastAccessed":"..."
> }
> ```

>  Check the dataSourceId for all the entries returned and note down the one that appears most.

[support-issue]: https://github.com/sanjacob/BlackboardSync/issues/new?assignees=sanjacob&labels=uni-new&projects=&template=uninew.yml&title=%5BNew+University%5D%3A+
[rdap-check]: https://74mxmsvvgqw6t23xycgaauf3cy0vyncw.lambda-url.eu-west-2.on.aws/
