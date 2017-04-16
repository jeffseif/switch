# switch

Scraping tools for getting me a damn Nintendo Switch

## Usage

```bash
git clone git@github.com:jeffseif/switch.git
cd switch
./cli --help
usage: main.py [-h] [--version] {all,amazon,target,walmart} ...

Scraping tools for getting me a damn Nintendo Switch

positional arguments:
  {all,amazon,target,walmart}
    all                 Check all
    amazon              Check amazon
    target              Check target
    walmart             Check walmart

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Version 1.0.0 | Jeffrey Seifried 2017
```

## Example

```bash
./cli all --beyond-console --zipcode=94703

> Amazon

✗ Gray Console
✗ Neon Console
✓ Breath of the Wild
Internet: https://www.amazon.com/dp/B01MS6MO77?qid=1492314650&m=A3IW5GL8H4PMF0&sr=1-0&ref_=pn_sr_sg_0_img_A3IW5GL8H4PMF0
✗ Pro Controller

> Target

✗ Gray Console
✗ Neon Console
✓ Breath of the Wild
San Francisco West: 2675 Geary Blvd, San Francisco, CA 94118-3400
Marin City: 180 Donahue St, Sausalito, CA 94965-1250
Pleasant Hill: 560 Contra Costa Blvd, Pleasant Hill, CA 94523-1216
San Leandro Bayfair: 15555 E 14th St, San Leandro, CA 94578-1978
Hayward North: 19661 Hesperian Blvd, Hayward, CA 94541-4200
Colma: 5001 Junipero Serra Blvd, Colma, CA 94014-3217
Daly City Serramonte: 133 Serramonte Ctr, Daly City, CA 94015-2349
Tanforan: 1150 El Camino Real, San Bruno, CA 94066-2420
San Ramon: 2610 Bishop Dr, San Ramon, CA 94583-2338
Albany: 1057 Eastshore Hwy, Albany, CA 94710-1011
Oakland-Emeryville: 1555 40th Street, Emeryville, CA 94608-3515
Alameda: 2700 Fifth Street, Alameda, CA 94501
Richmond: 4500 Macdonald Ave, Richmond, CA 94805-2307
Pinole: 1400 Fitzgerald Dr, Pinole, CA 94564-2250
San Francisco Central: 789 Mission St, San Francisco, CA 94103-3132

> Walmart

✗ Gray Console
✗ Neon Console
✗ Breath of the Wild
✓ Pro Controller
San Leandro Walmart: 1919 Davis St
San Leandro Walmart: 15555 Hesperian Blvd
```
