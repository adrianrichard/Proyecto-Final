Hansard
==========================
Hansard is the official report of all Parliamentary debates. Find Members, their
contributions, debates, petitions and divisions from published Hansard reports dating
back over 200 years. Daily debates from Hansard are published on this website the next
working day.

We've developed a little demo that takes these reports and converts them into beautifully formatted
pdf reports matching a lot of the structures and styling of the hansard website as of June 2024,

Take content from here, and make nice PDFs...

https://hansard.parliament.uk/

Hansard can be searched with a get request.  e.g. looking for a recent debate, do this:
  https://hansard.parliament.uk/search?searchTerm=western%20balkans


Run the example
==========================

1. Make an account on the [website](https://www.reportlab.com/accounts/register/) (needed for step 4)
2. Create a virtual environment (e.g. `python3.12 -m venv .`)
3. Activate the virtual environment (`. bin/activate`)
4. Install requirements (`pip install -r requirements.txt`) and use your username from step 1.
5. Run `python convert.py` (--url flag optional, must use hansard debate url. Examples are given below.)


To run default document, Security in the West Balkans:
==========================

$ `python convert.py`

In case you're offline we've included secwestbalkans_files so that example can be run fully.
You may need to adjust the code to read from a file again to do so however

To run a custom report:
==========================

1. download the html file and save it in the data/ directory
2. run convert.py with the arguments provided

current arguments:
	`--url` - the hansard url page you downloaded

Example document urls:
	https://hansard.parliament.uk/Commons/2024-05-02/debates/F7540B05-869A-40BD-9374-02F1D32A4BF7/SecurityInTheWesternBalkans
	https://hansard.parliament.uk/Commons/2024-05-24/debates/35765685-8E64-4885-B31D-9B4460A907E2/LeaseholdAndFreeholdReformBill
	https://hansard.parliament.uk/Commons/2024-05-15/debates/1B66A098-5488-44EE-9923-659A44A02121/BiodiversityLoss
	https://hansard.parliament.uk/Lords/2024-05-21/debates/C0DFBC16-BF81-4FC5-B7B0-B16FC6EB6452/WaterCompaniesFailure
	https://hansard.parliament.uk/Lords/2024-05-22/debates/E27EEF21-946C-4443-896D-616EF6BA374F/IsraelAndGaza
	https://hansard.parliament.uk/Lords/2024-05-21/debates/7919B99E-891F-4C6F-A9BD-93F130521BD7/RussiaSanctions

Example run:
	python convert.py --url="https://hansard.parliament.uk/Commons/2024-05-02/debates/F7540B05-869A-40BD-9374-02F1D32A4BF7/SecurityInTheWesternBalkans"

