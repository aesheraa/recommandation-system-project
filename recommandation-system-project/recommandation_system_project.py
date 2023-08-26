

#IMDB verileri kullanarak film tavsiye eden yapay zeka kodluyorum 
#Bu projede kulland���m  Recommendation system Temelinde iki algoritma yat�yor ;

#1-) User - Based Collaborative Filtering 

#- kullan�c�lar aras�ndaki benzerlik skorlar�n� bulmaya �al���r ku�llan�c� baz al�r.
#- her bir kullan�c�n�n sat�n ald��� veya izledi�i/dinledi�i metaryali kullan�c� bazl� olarak tutar ve bir matrise d�n��t�r�r.
#- bir kullan�c�ya(X) benzer ba�ka kullan�c�lar bulur.
#- X kullan�c�s�n�n hen�z izlemedi�i ancak benzer kullan�c�lar�n �o�unun izledi�i filmleri �nerir.
#- Kullan�c� bazl� oldu�u i�in maaliyetlidir. �nsan say�s� film say�s�ndan her zaman fazlad�r.( Netflix ya da IMDB deki kullan�c� say�s� milyonlarcad�r, filmler ise onbinlerce ya da daha azd�r.)

#2-) Item - Based Collaborative Filtering 

#- Kullan�c�lar yerine Itemleri baz al�r. Kullan�c�lar aras�ndaki ili�kiyle ilgilenmez. Itemler aras�ndaki ili�ki ve benzerlikle ilgilenir, birbirine benzeyen Itemleri bulur.
#- Itemler aras�nda benzerlik skorkar�n� bulmaya �al���r.
#- e�er filmleri seven ortak ki�iler varsa demek ki bu filmler birbirine benzer diye d���n�r ve benzerlik skorlar�n�k y�ksek belirler.

import numpy as np 
import pandas as pd 

column_names = ['user_id' , 'item_id' , 'rating' , 'timestamp']
df= pd.read_csv ( 'users.data ' , sep='/t' , names=column_names)

df.head()

#ka� kay�t varm�� g�relim
len(df)


#�imdi diger dosyam�z� y�kleyelim
movie_titles= pd.read_csv('movie_id_titles.csv')
movie_titles.head()


#ka� kay�t varm�� g�relim 
len(movie_titles)

df=pd.merge(df, movie_titles , on='item_id')
df.head()


# Recommandation Systemimi kuruyorum
# �ncelikle exceldeki pivot tablo benzeri bir yap� kuruyorum
# bu yap�ya g�re her kullan�c� bir sat�r olacak �ekilde yani datframe'imin index'i user_id olacak
# sutunlarda film isimleri ( yani title sutunu ) olacak 
# tablo i�inde de rating de�erleri olacak �ekilde bir dataframe olu�turuyorum 


moviemat= df.pivot_table(index='user_id' , columns='title ' , values='rating')
moviemat.head()

type(moviemat)


# amac�m  Star Wars filmine benzer film �nerileri yapmak 
# Star Wars  (1977) filminin user rating de�erlerine bak�yorum 
starwars_user_ratings = moviemat['Star Wars (1977)' ]
starwars_user_ratings.head()



#corrwith metodu kullanarak Star Wars filmi ile korelasyonlar� hesaplat�yorum :
similar_to_starwars= moviemat.corrwith(starwars_user_ratings)
similar_to_starwars
type(similar_to_starwars)



# baz� kay�tlarda bo�luklar oldu�u i�in hata veriyor similar_to_starwars bir seri, biz bunu corr_starwars isimli bir dataframe'e d�n��t�relim  ve NaN kay�tlar�n� temizleyip bakal�m
corr_starwars= pd.DataFrame(similar_to_starwars , columns=[ 'Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars.head()



# elde etti�imiz datframe'i s�ralayal�m ve tavsiyelerine bakal�m 
corr_starwars.sort_values('Correlation' , ascending= False).head(10)



# alakas�z sonu�lar verdi ��nk� �ok az oy alm�� filmleri bile i�leme dahil etti, bunu engellemek i�in 100 den az oy alan fillmleri eliyorum 
# ratings isimli bir dataframe oluturuyorum ve her filmin ka� oy ald���n� ( oy say�lar�n� ) tutuyorum 




df.head()


# timestamp sutununa ihtiyac�m yok onu siliyorum 
df.drop(['timestamp'] , axis=1 )



# her filmin ortalama (mean value) rating de�erini buluyorum
ratings =pd.DataFrame(df.groupby('title')['rating'].mean())



# b�y�kten k����e s�ralay�p bak�yorum 
ratings.sort_values('rating' , ascending=False).head()



# bu ortalamalar hesaplan�rken ka� oy ald���na bakmad�k o y�zden hi� bilinmeyen filmler �nerdi
# �imdi her filmin ald��� oy say�s�n� bulal�m 
ratings[ 'rating_oy_sayisi']=pd.DataFrame(pd.groupby('title')['rating'].count())
ratings.head()



# �imdi en �ok oy alan filmleri b�y�ktrn k����e s�ralayal�m 
ratings.sort_values('rating_oy_sayisi' , ascending=False).head()



#  as�l amac�ma d�n�yorum ve corr_starwars datframe'ime  rating_oy_sayisi sutununu ekliyorum ( join ile )
corr_starwars.sort_values('Correlation', ascending=False).head(10)
corr_starwars= corr_starwars.join(ratings['rating_oy_sayisi']) 
corr_starwars.head()




# sonuca bakal�m 
corr_starwars[corr_satarwars['rating_oy_sayisi ']>100.sort_values('Correlation' , ascending=False)].head()
