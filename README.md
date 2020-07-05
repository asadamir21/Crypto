# Crypto
### SECURE  TRANSMISSION OF DATA USING CRYPTOGRAPHY & SEYGNOGRAPHY
<p align="justify">
   Data security has become a major resource nowadays for effective handling of various demand for any organization. One of those networks is the most important demand to supply secure data transmission from one place to another. Cryptography is among the mechanisms that are the safest way to transfer sensitive information seemed to receiver. Its major aim is to create sensitive information unreadable to all  un-authorized users except the supposed receiver.
To enhance security there is a need to provide a two-layer approach to provide a better and better security. Cryptography is concerned with the security of transmitting data and allows it to communicate secretly by hiding data within the data (text / image). Steganography is the process of hiding the presence of a secret-message, so that no one can see the hidden message.
Steganography combined with cryptography is a powerful tool which is enabling people to communicate without possible eavesdroppers; the proposed method provides acceptable image quality with a few distortions in the image.
</p>

### ABOUT:
<p align="justify">
   In our project we are going to implement algorithms of a research paper , in which a method for protection data was proposed comprises a hybridization between cryptography and steganography. In the proposed approach particle swarm optimization algorithm (PSO) was used in both methods(encryption and steganography).The PSO algorithm was used in key generation process for data encryption and in generating hidden locations for data hiding. Also, the Least Significant Bit (LSB) was utilized to add the encrypted data into LSB of the cover and the PSO was utilized to specify the location of hiding data.
</p>

#### EXISTING SYSTEM:
<p align="justify">
   Asymmetric encryption algorithms are almost 1000 times slower than symmetric encryption algorithms, because they require more computational processing power. So symmetric encryption algorithms are commonly used now days; but cryptography isn’t able to hide the presenting of data alone and it can’t protect data effectively. Any eavesdropper can easily detect the presence of encrypted data and can try several attacks in order to get the original data.
</p>

#### PROBLEM SOLUTION:
<p align="justify">
   To enhance the security there is a need to provide two-layer approach for providing an improved and better security. Steganography is concerned with security of transmitting data and allows communicating secretly by hiding the data within data (text/image) . Steganography is the process of hiding the presence of a secret-message, so that no one will see the hiding message.
We are designing a security mechanism to remove all the all the security attacks  by using a hybrid technique of steganography and cryptography which is more secure way for transmission of text data in the form of image. 
</p>

#### SYSTEM  WORKING:
<p align="justify">
   We are developing an application which will be used for secure transmission of sensitive text data. user can type a text then select a image then application encrypt text message using PSO algorithms  then  hide encrypted text  into  image using LSB technique of steganography send the stego-image to  supposed user. On other side decrypt image to text by using steam cipher technique.
</p>

#### Modules

1. ##### Data Entry:
   Firstly the user should enter text data which he wants to send to supposed user.
2. ##### Data Encryption:
   This entered text data is then converted into the cipher text by using PSO algorithm.
3. ##### Cover image Selection:
   The user selects a cover image for data hiding and the size of Image should be enough to hide data.
4. ##### LSB Hiding:
   The LSB technique of steganography will be used for Data Hiding in image.
5. ##### Data Transmission:
   The stego image will be transmitted through the network and the authenticate user will receive it.
6. ##### LSB Extraction:
   Read the cover image data secret location generated by the algorithms. After that character of secret message will be retrieved in the form of cipher text.
7. ##### Data Decryption:
   The cipher text is decrypted into the original text message.

### Advantages
1.  Cryptography and steganography are combined in order to increase the strength of the algorithm
2.  Very secure, hard to detect
3.  Strong current algorithms are currently resistant to attack, increases the security and robustness against the attacks
4.  Both methods provide security; to add multiple layers of security it is always a good practice to use Cryptography and Steganography together. It is better than the technique used separately.
5.  Reasonable Cost. 
6.  Main Characteristics:
7.  Flexibility, II. Simplicity

### System Implementation
1.	Backend database used will be MYSQL
2.	Frontend and Backend coding is done in PYTHON
