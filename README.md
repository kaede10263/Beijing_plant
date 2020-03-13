# Beijing_plant
 
Web_scrapy for Beijing_plant.We test spray for this project.

First,scrapying the data in need .

Second,Compare the same ScienceName and combine the useful data.

The data we need is 
<img src="https://github.com/kaede10263/Beijing_plant/blob/master/picture/Image.png"/>

[Source url](http://tai2.ntu.edu.tw/PlantInfo.php)


## envirment
*   python = 3.6
*   scrapy = 2.0.0
*   numpy = 1.14.3
*   pandas = 0.23.0

## install
Install anaconda and add anaconda into envirment path.
```
conda create --name myenv python=3.6
```

clone this github and activate VM
```
activate myenv
```

and run this 

``` 
pip install -r requirements.txt
``` 



## command use
here is the folder

``` 
cd  D:\GDbackup\PROJECT\tree\Beijing_plant\plant_crawler
```
do this command

```
scrapy crawl plant_spyder
```

You will get "hello.csv" in the path.

```
python combine.py
```

You will get "result.csv" in the path.