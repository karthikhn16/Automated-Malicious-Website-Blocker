import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from cryptography.fernet import Fernet
import ctypes
import os
import platform
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import re
import sys

stored_url = None
stored_url1 = None
@csrf_exempt
def capture_url(request):
    global stored_url,stored_url1
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            url = re.sub(r'^https?://', '', url)
            url = re.sub(r'www.', '', url)

            url = re.sub(r'/.*', '', url)
            url1 = url
            print("URL::::",url)
                     
            if not url.startswith('www.'):
                url1 = 'www.' + url
                print('URL1::::',url1)
            print("I AM CALLED WITH THE URL",url)
            stored_url = url
            stored_url1 = url1

            
            #  CHECKING URL EXISTS OR NOT
            existencecheck=urlexist(url)
            if existencecheck:
                print("I returnned a response")
                return JsonResponse({'status': 'error', 'message': 'valid','existencecheck':existencecheck})
                

            if url:
                vt_url = "https://www.virustotal.com/vtapi/v2/url/report"
                params = {'apikey': 'cfe8376fcbed5b2507893ec71bfa73508d72b98e6efd22a9be9cef6bcafb6d5e', 'resource': url}
                response = requests.get(vt_url, params=params)
                result = response.json()
              
                # print(result)
                if result['response_code'] == 1:
                    positives = result.get('positives', 0)
                    print("THE RESULT IS :",positives)
                    total = result.get('total', 0)
                    if positives > 0:
                        # messagebox.showinfo("Warning", "This is malicious website which will be blocked")
                        print(f"Malicious. {positives}/{total} scans reported this URL as malicious.")
                        # code to block website
                        if not url:
                            messagebox.showwarning("Warning", "Please enter a URL.")
                            return
                        try:
                            if not (existencecheck): 
                                os.system("runas /user:administrator " + sys.executable + " " + ' '.join(sys.argv))
                                with open(r"C:\Windows\System32\drivers\etc\hosts", 'a') as hosts_file:
                                    hosts_file.write(f"\n127.0.0.1\t{url1}\n")
                                    hosts_file.write(f"\n127.0.0.1\t{url}\n")
                            return JsonResponse({'status': 'error', 'message': 'valid','existencecheck':existencecheck})
                            
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to block the URL: {e}")
                    else:
                        print("RECIEVED URL IS NOT A MALICIOUS")
                        # messagebox.showinfo("Message", "This is not a malicious website so no need to block")
                else:
                    return JsonResponse({'status': 'error', 'message': 'URL not found in VirusTotal database.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No URL provided'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@csrf_exempt
def unblock_url(request):
     global stored_url,stored_url1
     if request.method == 'GET':
        print("URL IS",stored_url)
        with open(r'C:\Windows\System32\drivers\etc\hosts', 'r') as file:
            lines = file.readlines()
            
        lines = [line for line in lines if stored_url not in line and stored_url1 not in line]
        print(lines)
        with open(r'C:\Windows\System32\drivers\etc\hosts', 'w') as file:
                
                file.writelines(lines)

        return JsonResponse({'status': 'success', 'url': stored_url, 'url1': stored_url1})



def urlexist(url):
    try:
        with open(r'C:\Windows\System32\drivers\etc\hosts', 'r') as file:
            print("Using for loop to check each line in the file")
            for line in file:
                if url in line:
                    print(line.strip())
                    return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False





































# Create the main window
# window = tk.Tk()
# window.title("Email and Password Validation")

# # Set window size and center it
# window.geometry("700x800")
# window.eval('tk::PlaceWindow . center')

# try:
#     # Add image using PIL
#     image_path = r"D:\Downloads\WDk8fMQ3geiQdb8LG6gw27.jpg"
#     image = Image.open(image_path)
#     image = image.resize((700, 500))  # Resize the image as needed
#     photo = ImageTk.PhotoImage(image)
#     image_label = tk.Label(window, image=photo)
#     image_label.image = photo  # Keep a reference to the image to prevent garbage collection
#     image_label.pack()
# except Exception as e:
#     messagebox.showerror("Error", f"Failed to load image: {e}")

# # Create input fields
# label1 = tk.Label(window, text="Email ID:", font=("Arial", 14))
# label1.pack()
# entry1 = tk.Entry(window, font=("Arial", 14))
# entry1.pack()

# button = tk.Button(window, text="Get Encrypted Password", font=("Arial", 14), command=perform_operation)
# button.pack()

# label2 = tk.Label(window, text="Password:", font=("Arial", 14))
# label2.pack()
# entry2 = tk.Entry(window, font=("Arial", 14), show="*", state='disabled')  # Initially disabled
# entry2.pack()

# buttonverify = tk.Button(window, state='disabled', text="Verify!", font=("Arial", 14), command=validate_password)
# buttonverify.pack()

# label3 = tk.Label(window, text="URL:", font=("Arial", 14))
# label3.pack()
# entry3 = tk.Entry(window, font=("Arial", 14), state='normal')  # Initially disabled
# entry3.pack()

# buttonforblocking = tk.Button(window, state='normal', text="Block Website", font=("Arial", 14), command=Blockwebsite)
# buttonforblocking.pack()

# Run the application
# window.mainloop()
