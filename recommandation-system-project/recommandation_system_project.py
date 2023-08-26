

#IMDB verileri kullanarak film tavsiye eden yapay zeka kodluyorum 
#Bu projede kullandýðým  Recommendation system Temelinde iki algoritma yatýyor ;

#1-) User - Based Collaborative Filtering 

#- kullanýcýlar arasýndaki benzerlik skorlarýný bulmaya çalýþýr kuýllanýcý baz alýr.
#- her bir kullanýcýnýn satýn aldýðý veya izlediði/dinlediði metaryali kullanýcý bazlý olarak tutar ve bir matrise dönüþtürür.
#- bir kullanýcýya(X) benzer baþka kullanýcýlar bulur.
#- X kullanýcýsýnýn henüz izlemediði ancak benzer kullanýcýlarýn çoðunun izlediði filmleri önerir.
#- Kullanýcý bazlý olduðu için maaliyetlidir. Ýnsan sayýsý film sayýsýndan her zaman fazladýr.( Netflix ya da IMDB deki kullanýcý sayýsý milyonlarcadýr, filmler ise onbinlerce ya da daha azdýr.)

#2-) Item - Based Collaborative Filtering 

#- Kullanýcýlar yerine Itemleri baz alýr. Kullanýcýlar arasýndaki iliþkiyle ilgilenmez. Itemler arasýndaki iliþki ve benzerlikle ilgilenir, birbirine benzeyen Itemleri bulur.
#- Itemler arasýnda benzerlik skorkarýný bulmaya çalýþýr.
#- eðer filmleri seven ortak kiþiler varsa demek ki bu filmler birbirine benzer diye düþünür ve benzerlik skorlarýnýk yüksek belirler.

import numpy as np 
import pandas as pd 

column_names = ['user_id' , 'item_id' , 'rating' , 'timestamp']
df= pd.read_csv ( 'users.data ' , sep='/t' , names=column_names)

df.head()

#kaç kayýt varmýþ görelim
len(df)


#þimdi diger dosyamýzý yükleyelim
movie_titles= pd.read_csv('movie_id_titles.csv')
movie_titles.head()


#kaç kayýt varmýþ görelim 
len(movie_titles)

df=pd.merge(df, movie_titles , on='item_id')
df.head()


# Recommandation Systemimi kuruyorum
# öncelikle exceldeki pivot tablo benzeri bir yapý kuruyorum
# bu yapýya göre her kullanýcý bir satýr olacak þekilde yani datframe'imin index'i user_id olacak
# sutunlarda film isimleri ( yani title sutunu ) olacak 
# tablo içinde de rating deðerleri olacak þekilde bir dataframe oluþturuyorum 


moviemat= df.pivot_table(index='user_id' , columns='title ' , values='rating')
moviemat.head()

type(moviemat)


# amacým  Star Wars filmine benzer film önerileri yapmak 
# Star Wars  (1977) filminin user rating deðerlerine bakýyorum 
starwars_user_ratings = moviemat['Star Wars (1977)' ]
starwars_user_ratings.head()



#corrwith metodu kullanarak Star Wars filmi ile korelasyonlarý hesaplatýyorum :
similar_to_starwars= moviemat.corrwith(starwars_user_ratings)
similar_to_starwars
type(similar_to_starwars)



# bazý kayýtlarda boþluklar olduðu için hata veriyor similar_to_starwars bir seri, biz bunu corr_starwars isimli bir dataframe'e dönüþtürelim  ve NaN kayýtlarýný temizleyip bakalým
corr_starwars= pd.DataFrame(similar_to_starwars , columns=[ 'Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars.head()



# elde ettiðimiz datframe'i sýralayalým ve tavsiyelerine bakalým 
corr_starwars.sort_values('Correlation' , ascending= False).head(10)



# alakasýz sonuçlar verdi çünkü çok az oy almýþ filmleri bile iþleme dahil etti, bunu engellemek için 100 den az oy alan fillmleri eliyorum 
# ratings isimli bir dataframe oluturuyorum ve her filmin kaç oy aldýðýný ( oy sayýlarýný ) tutuyorum 




df.head()


# timestamp sutununa ihtiyacým yok onu siliyorum 
df.drop(['timestamp'] , axis=1 )



# her filmin ortalama (mean value) rating deðerini buluyorum
ratings =pd.DataFrame(df.groupby('title')['rating'].mean())



# büyükten küçüðe sýralayýp bakýyorum 
ratings.sort_values('rating' , ascending=False).head()



# bu ortalamalar hesaplanýrken kaç oy aldýðýna bakmadýk o yüzden hiç bilinmeyen filmler önerdi
# þimdi her filmin aldýðý oy sayýsýný bulalým 
ratings[ 'rating_oy_sayisi']=pd.DataFrame(pd.groupby('title')['rating'].count())
ratings.head()



# þimdi en çok oy alan filmleri büyüktrn küçüðe sýralayalým 
ratings.sort_values('rating_oy_sayisi' , ascending=False).head()



#  asýl amacýma dönüyorum ve corr_starwars datframe'ime  rating_oy_sayisi sutununu ekliyorum ( join ile )
corr_starwars.sort_values('Correlation', ascending=False).head(10)
corr_starwars= corr_starwars.join(ratings['rating_oy_sayisi']) 
corr_starwars.head()




# sonuca bakalým 
corr_starwars[corr_satarwars['rating_oy_sayisi ']>100.sort_values('Correlation' , ascending=False)].head()
