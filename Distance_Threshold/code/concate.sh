# {1} the top root folder 



for i in $(ls ${1})
do
	NUM=${i//[^0-9]/}  # Extract the number 
	echo $1/$i/$NUM.all
	ls $1/$i/*.closest.* | sort -V
	#cat $(ls $1/$i/*.closest.*| sort -V) > $1/$i/$NUM.all
done