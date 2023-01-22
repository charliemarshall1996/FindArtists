
try:
    import pandas as pd
    import requests
    import json
    from json import JSONDecodeError
    from datetime import datetime
    import os
    import time
except ImportError as err:
    print("Import Error: " + str(err) + "programme terminated.")
except ImportWarning as err:
    print("Import Warning: " + str(err))


#Main Info
first_names = []
last_names = []
profile_url = []
#countries = []
#genders = []
#activities = []

#I4B Info
#i4b_guid = []
#i4b_companies = []
i4b_company_guids = []
i4b_company_countries = []
i4b_company_aliases = []
i4b_title = []

#Experience 1 Info
exp1_start_dates = []
exp1_end_dates = []
exp1_companies = []
exp1_company_urls = []
exp1_titles = []

#Experience 2 Info
exp2_start_dates = []
exp2_end_dates = []
exp2_companies = []
exp2_company_urls = []
exp2_titles = []

#Experience 3 Info
exp3_start_dates = []
exp3_end_dates = []
exp3_companies = []
exp3_company_urls = []
exp3_titles = []

#Experience 4 Info
exp4_start_dates = []
exp4_end_dates = []
exp4_companies = []
exp4_company_urls = []
exp4_titles = []

#Experience 5 Info
exp5_start_dates = []
exp5_end_dates = []
exp5_companies = []
exp5_company_urls = []
exp5_titles = []

#Error files:
error_code = []
error_link = []

company_looked_at = []

dire = str(os.getcwd())
default_input_path = dire + '.\\Test Data'
default_output_path = dire + '.\\ProxyPull Exported Files'
default_suppression_path = dire + '.\\Suppression File'

class ProxyPull:
    
    def __init__(self, input_filename, proxy_curl_key, google_key, se_id, cc_or_cd, output_filename, search_terms, suppression_filename, input_filepath=default_input_path, output_filepath=default_output_path, suppression_filepath=default_suppression_path):
        #Initialise Input Values
        self.input_filename = input_filename
        self.input_filepath = input_filepath
        self.proxy_curl_key = proxy_curl_key
        self.cc_or_cd = cc_or_cd
        self.output_filename = output_filename
        self.output_filepath = output_filepath
        self.search_terms = search_terms
        self.suppression_filename = suppression_filename
        self.suppression_filepath = suppression_filepath
        self.se_id = se_id
        self.google_key = google_key
    
    def pull(self):
        #Compiles functions, defines flow
        try:
            print("Starting Pull.")
            linkedin_links = self.get_links() #Get linkedin links
            print("Found " + str(len(linkedin_links)) + " links to process.")
            self.retrieve_profile_info(linkedin_links) #Append profile info
            print("Got all profiles.")
            self.export_error_file() #Output error file
            self.export_main_file() #Output main file
            companies_num = len(set(i4b_company_guids))
            print(f"Process Completed. Found {len(profile_url)} contacts across {companies_num} companies.")
        except RuntimeError:
            try:
                self.export_main_file()
            except:
                pass
            print("Runtime Error: Programme Terminated. Please contact developer.")
        except KeyboardInterrupt:
            try:
                self.export_main_file()
                print("File exported.")
            except:
                pass
                print("Unable to export file.")
            print("Keyboard Interrupt: Programme Terminated.")
        except AttributeError:
            try:
                self.export_main_file()
                print("File exported.")
            except:
                pass
                print("Unable to export file.")
            print("Attribute Error: Programme Terminated. Please contact developer.")
        except WindowsError:
            try:
                self.export_main_file()
                print("File exported.")
            except:
                pass
                print("Unable to export file.")
            print("Windows Error: Programme Terminated. Please try again.")
        except FutureWarning:
            try:
                self.export_main_file()
                print("File exported.")
            except:
                pass
                print("Unable to export file.")
            print("Future Warning: Please contact developer.")
        except RuntimeWarning as err:
            try:
                self.export_main_file()
                print("File exported.")
            except:
                pass
                print("Unable to export file.")
            print("Runtime Warning: Please contact developer.")
        except TypeError as err:
            try:
                self.export_main_file()
                print("File exported.")
            except:
                pass
                print("Unable to export file.")
            print("Type Error: " + str(err) + " Please check input parameters.")

    def get_links(self):
        suppression_links = self.extract_suppression_file()
        print('Checking project type')
        #Check project type
        print('Getting Links')
        if self.cc_or_cd == 'CC':
            contacts_to_check = self.extract_file(self.input_filename) #Extract specified CC file
            linkedin_links = contacts_to_check['Contact LinkedIn'].tolist() #List all linkedin links to check given in CC file
        
        elif self.cc_or_cd == 'CD':
            linkedin_links = [] #Define list for links
            extracted_companies = self.extract_file(self.input_filename, self.input_filepath) #Extract specified CD file
            companies_df = pd.DataFrame(extracted_companies)
            for row in companies_df.itertuples():
                i4b_id = row[3]
                company = row[6]
                country = row[9]
                linkedin_links.extend(self.search_companies(i4b_id, country, company, suppression_links)) #Need to change defined search terms to terms taken from spreadsheet
            link_num = len(linkedin_links)
            print(str(link_num) + " links found") #Tell us how many links were found
        else:
            print('Invalid Project Type. Please check filepath and filetype.') #Error message if filetype/path is incorrect.
        
        return linkedin_links
    
    def search_companies(self, i4b_id, country, company, suppression_links):
        print('Searching terms')
        #Search Params
        country = "uk"
        links = []

        #Calculate page
        page = 1
        #Search engine options
        options = {
                'method' : 'get',
                'contentType': 'application/json',
                }
        #Send request
        #Search query
        for term in self.search_terms: #For each defined term
            print("Finding contacts at " + company + " for " + term) #Tell us what company and term is being looked at
            query = f"site:{country}.linkedin.com/in intitle:{term}{company}{country}" #Create query to search google for
            
            while 0 < 1: #Infinite loop until specified break
                print("Starting infinite loop.")
                start = (page - 1) * 10 + 1 #Calculate starting index to request
                if page <= 2: #If page number is less than or equal to defined value
                    print("Getting page " + str(page))
                    response = requests.get(f"https://www.googleapis.com/customsearch/v1/siterestrict?key={self.google_key}&start={start}&q={query}&exactTerms={company}&cx={self.se_id}&cr={country}", options) #Request with query
                    print("Page " + str(page) + " received.")
                    time.sleep(0.5) #This avoids QPS Limit
                    results = json.loads(response.text) #Get response text, turn into JSON
                    print("Got results")
                    try:
                        results_info = results['searchInformation'] #Get information regarding search results (amount of search results etc.)
                        total_results = results_info['totalResults'] #Tell us how many results available
                        print('total results' + str(total_results)) #Print total results
                        if int(total_results) == 0: #If no results available
                                print('No more results for company') #Tell us why we can't get that page
                                break
                        else:    
                            try:
                                print("looping profiles")
                                profiles = results['items'] #Find number of profiles from JSON dictionary
                                for profile in profiles:
                                    try:
                                        link = profile['link'] #Find profile link for each profile
                                        link_suffix = link.split('/in/', 1)[1] #Find suffix of link to check against suppression file
                                        suppression = self.suppress(link_suffix, suppression_links)
                                        if suppression == True: #Check against suppression file
                                            pass
                                        else:
                                            links.append(link) #Apped link to links list
                                            company_looked_at.append(company)
                                            #i4b_companies.append(company) #Append company searched for
                                            #i4b_company_guids.append(i4b_id)
                                            #i4b_company_countries.append(country)
                                    except:
                                        pass
                            except:
                                print("Dict Error Page:" + str(page)) #Tell us there was an error in returning page
                                pass
                            page += 1 #Add one to page number to change starting index
                    except KeyError:
                        print("Google returned unexpected JSON file for search at " + company + " for " + term + " on page: " + str(page))
                        error_info = results["error"]
                        code = error_info["code"]
                        print(self.error_check_google(str(code)))
                        page += 1 #Add one to page number to change starting index
                        break
                    except:
                        pass
                else:
                    break
        return links #Return links
    
    def suppress(self, link_suffix, suppression_links):
        print("Checking Against Suppression File.")        
        suppressed_total = 0
        try:
            if any(link_suffix in suppressed for suppressed in suppression_links):
                print("Contact Suppressed:" + link_suffix)
                suppressed_total += 1
                suppressed = True
            else:
                print("Contact Not Suppressed:" + link_suffix)
                suppressed = False
            #print(suppressed_total + " links suppressed.")
            return suppressed
        except:
            print("Suppression error: " + link_suffix)
            suppressed = False
            return suppressed
        
    def extract_suppression_file(self):
        print('Extracting Suppression File')
        suppression_file = self.extract_file(self.suppression_filename, self.suppression_filepath)
        suppression_links = suppression_file['LinkedIn_URL'].tolist()
        print('Suppression file extracted.')
        return suppression_links

    def extract_file(self, filename, filepath):
        #Try extracting the defined input spreadsheet
        try:
            if '.xlsx' in filename: #If '.xlsx' is in the filename
                extracted_file = pd.read_excel(f'{filepath}\\{filename}', index_col=False) #Extract as excel file
            elif '.csv' in filename: #If '.csv' is in the filename
                extracted_file = pd.read_csv(f'{filepath}\\{filename}', index_col=False, engine='python', encoding='UTF-8') #Extract as csv
            return extracted_file #Return the file
        except pd.errors.EmptyDataError:
            print("No data to extract in file:" + filename)
        except FileNotFoundError: #Need to define exception type
            print('Invalid file. Please check name or filepath:' + filename)
        except pd.errors.PerformanceWarning as err:
            print("Potential performance impact:" + filename + " " + str(err))
        except pd.errors.ParserError as err:
            print("Error parsing file:" + filename + " " + str(err))
        except pd.errors.DtypeWarning as err:
            print("Input file contains multiple data types in single column:" + filename + " " + str(err))
        except UnicodeDecodeError as err:
            print("Error extracting file:" + filename + " " + str(err))
        except:
            print("Unknow Error, please contact developer:" + filename)
        
    def retrieve_profile_info(self, linkedin_links):
        for link in linkedin_links:
            try:
                print("Retrieving Profile info for: " + link)
                #Connect to profile, return dict
                print("Getting Dictionary")
                try:
                    dict = self.retrieve_dict(link)
                    profile_url.append(link)
                except:
                    print("error receiving dict")
                    profile_url.append('NULL')
                    pass
                
                #Collect Experience Info
                try:
                    print("Getting Experiences")
                    experiences = dict['experiences']
                    experience_len = len(experiences)
                    self.experience_get(experiences, experience_len)
                except:
                    exp1_start_dates.append('NULL - ERROR')
                    exp1_end_dates.append('NULL - ERROR')
                    exp1_companies.append('NULL - ERROR')
                    exp1_company_urls.append('NULL - ERROR')
                    exp1_titles.append('NULL - ERROR')
                    exp2_start_dates.append('NULL - ERROR')
                    exp2_end_dates.append('NULL - ERROR')
                    exp2_companies.append('NULL - ERROR')
                    exp2_company_urls.append('NULL - ERROR')
                    exp2_titles.append('NULL - ERROR')
                    exp3_start_dates.append('NULL - ERROR')
                    exp3_end_dates.append('NULL - ERROR')
                    exp3_companies.append('NULL - ERROR')
                    exp3_company_urls.append('NULL - ERROR')
                    exp3_titles.append('NULL - ERROR')
                    exp4_start_dates.append('NULL - ERROR')
                    exp4_end_dates.append('NULL - ERROR')
                    exp4_companies.append('NULL - ERROR')
                    exp4_company_urls.append('NULL - ERROR')
                    exp4_titles.append('NULL - ERROR')
                    exp5_start_dates.append('NULL - ERROR')
                    exp5_end_dates.append('NULL - ERROR')
                    exp5_companies.append('NULL - ERROR')
                    exp5_company_urls.append('NULL - ERROR')
                    exp5_titles.append('NULL - ERROR')

                #Collect standard Info
                print("Collecting General Info")
                try:
                    first_name = dict['first_name']
                    first_names.append(first_name) #Append first name to first names list
                except:
                    first_names.append('NULL')
                try:
                    last_name = dict['last_name']
                    last_names.append(last_name) #Append last name to last names list
                except:
                    last_names.append('NULL')
            except:
                print("error retrieving contact at " + link)
                pass
            print( #Print number of dictionary items for each key in the dictionary. Unecessary. Checks for inconsistent record values.
                "First Name" + str(len(first_names)), 
                "Last Name" + str(len(last_names)), 
                "Profile URL" + str(len(profile_url)), 
                "exp 1 start" + str(len(exp1_start_dates)), 
                "exp 1 end" + str(len(exp1_end_dates)), 
                "exp 1 url" + str(len(exp1_company_urls)), 
                "exp 1 company" + str(len(exp1_companies)),
                "exp 1 title" + str(len(exp1_titles)),
                "exp 2 start" + str(len(exp2_start_dates)),
                "exp 2 end" + str(len(exp2_end_dates)),
                "exp 2 url" + str(len(exp2_company_urls)),
                "exp 2 company" + str(len(exp2_companies)),
                "exp 2 title" + str(len(exp2_titles)),
                "exp 3 start " + str(len(exp3_start_dates)),
                "exp 3 end" + str(len(exp3_end_dates)),
                "exp 3 url" + str(len(exp3_company_urls)),
                "exp 3 company" + str(len(exp3_companies)),
                "exp 3 title" + str(len(exp3_titles)),
                "exp 4 start" + str(len(exp4_start_dates)),
                "exp 4 end" + str(len(exp4_end_dates)),
                "exp 4 company" + str(len(exp4_companies)),
                "exp 4 title" + str(len(exp4_titles)),
                "exp 5 start" + str(len(exp5_start_dates)),
                "exp 5 end" + str(len(exp5_end_dates)),
                "exp 5 url" + str(len(exp5_company_urls)),
                "exp 5 company" + str(len(exp5_companies)),
                "exp 5 title" + str(len(exp5_titles))
                )
            if len(profile_url) != len(exp1_start_dates):
                quit()
            else:
                pass

    def retrieve_dict(self, link):

        header_dic = {'Authorization': 'Bearer ' + self.proxy_curl_key} #Define request headers
        response = requests.get('https://nubela.co/proxycurl/api/v2/linkedin', params={'url': link}, headers=header_dic) #Send request to Proxycurl

        #Is the response valid?
        try:
            #Return JSON dict
            return json.loads(response.text)
        except JSONDecodeError:
            self.error_check_curl(response.text) #Check for Proxycurl errors
            error_code.append(self.error_check_curl(response.text)) #Append error to code list
            error_link.append(link) #Append link that returned error
        except KeyError:
            self.error_check_curl(response.text) #Check for Proxycurl errors
            error_code.append(self.error_check_curl(response.text)) #Append error to code list
            error_link.append(link)

    def date_parse(self, full_date):
        day = full_date['day'] #Extract Day val
        month = full_date['month'] #Extract Month val
        year = full_date['year'] #Extract Year val
        
        #Add leading zero if less than 10
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        #Add leading zero to month if less than ten
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        #Concatanate results into single string    
        date = str(day) + '/' + str(month) + '/' + str(year)

        #Return date
        return date
    
    def experience_get(self, experiences, experience_len):
        print(experience_len)
        try:  
            counter = 0 
            #Append empty string to list, depending on amount of experiences
            if experience_len < 1:
                exp1_start_dates.append('NULL')
                exp1_end_dates.append('NULL')
                exp1_companies.append('NULL')
                exp1_company_urls.append('NULL')
                exp1_titles.append('NULL')
                exp2_start_dates.append('NULL')
                exp2_end_dates.append('NULL')
                exp2_companies.append('NULL')
                exp2_company_urls.append('NULL')
                exp2_titles.append('NULL')
                exp3_start_dates.append('NULL')
                exp3_end_dates.append('NULL')
                exp3_companies.append('NULL')
                exp3_company_urls.append('NULL')
                exp3_titles.append('NULL')
                exp4_start_dates.append('NULL')
                exp4_end_dates.append('NULL')
                exp4_companies.append('NULL')
                exp4_company_urls.append('NULL')
                exp4_titles.append('NULL')
                exp5_start_dates.append('NULL')
                exp5_end_dates.append('NULL')
                exp5_companies.append('NULL')
                exp5_company_urls.append('NULL')
                exp5_titles.append('NULL')
            elif experience_len == 1:
                exp2_start_dates.append('NULL')
                exp2_end_dates.append('NULL')
                exp2_companies.append('NULL')
                exp2_company_urls.append('NULL')
                exp2_titles.append('NULL')
                exp3_start_dates.append('NULL')
                exp3_end_dates.append('NULL')
                exp3_companies.append('NULL')
                exp3_company_urls.append('NULL')
                exp3_titles.append('NULL')
                exp4_start_dates.append('NULL')
                exp4_end_dates.append('NULL')
                exp4_companies.append('NULL')
                exp4_company_urls.append('NULL')
                exp4_titles.append('NULL')
                exp5_start_dates.append('NULL')
                exp5_end_dates.append('NULL')
                exp5_companies.append('NULL')
                exp5_company_urls.append('NULL')
                exp5_titles.append('NULL')
            elif experience_len == 2:
                exp3_start_dates.append('NULL')
                exp3_end_dates.append('NULL')
                exp3_companies.append('NULL')
                exp3_company_urls.append('NULL')
                exp3_titles.append('NULL')
                exp4_start_dates.append('NULL')
                exp4_end_dates.append('NULL')
                exp4_companies.append('NULL')
                exp4_company_urls.append('NULL')
                exp4_titles.append('NULL')
                exp5_start_dates.append('NULL')
                exp5_end_dates.append('NULL')
                exp5_companies.append('NULL')
                exp5_company_urls.append('NULL')
                exp5_titles.append('NULL')
            elif experience_len == 3:
                exp4_start_dates.append('NULL')
                exp4_end_dates.append('NULL')
                exp4_companies.append('NULL')
                exp4_company_urls.append('NULL')
                exp4_titles.append('NULL')
                exp5_start_dates.append('NULL')
                exp5_end_dates.append('NULL')
                exp5_companies.append('NULL')
                exp5_company_urls.append('NULL')
                exp5_titles.append('NULL')
            elif experience_len == 4:
                exp5_start_dates.append('NULL')
                exp5_end_dates.append('NULL')
                exp5_companies.append('NULL')
                exp5_company_urls.append('NULL')
                exp5_titles.append('NULL')
            else:
                pass
                
            for experience in experiences: #For each experience
                counter += 1
                if counter == 1: #If index is zero
                    try: #Try finding/parsing start date
                        start_date = experience['starts_at']
                        exp1_start_date = self.date_parse(start_date)
                    except: #If it can't, return 
                        exp1_start_date = 'NULL'

                    try:
                        end_date = experience['ends_at']
                        exp1_end_date = self.date_parse(end_date)

                    except:
                        if exp1_start_date != 'NULL': #If the start date is NOT 
                            exp1_end_date = 'Present' #Assume the end date is present
                        else:
                            exp1_end_date = 'NULL' 
                    
                    exp1_start_dates.append(exp1_start_date) #Append start date to start dates list
                    exp1_end_dates.append(exp1_end_date) #Append end date to end dates list
                    exp1_companies.append(experience['company']) #Append company to company dates list
                    exp1_company_urls.append(experience['company_linkedin_profile_url']) #Append company linkedin URL to company linkedin URLs list
                    exp1_titles.append(experience['title']) #Append titles to tiles list
                elif counter == 2: #If Index is 1
                    try:
                        start_date = experience['starts_at']
                        exp2_start_date = self.date_parse(start_date)
                    except:
                        exp2_start_date = 'NULL'

                    try:
                        end_date = experience['ends_at']
                        exp2_end_date = self.date_parse(end_date)

                    except:
                        if exp2_start_date != 'NULL':
                            exp2_end_date = 'Present'
                        else:
                            exp2_end_date = 'NULL'
                    
                    exp2_start_dates.append(exp2_start_date)
                    exp2_end_dates.append(exp2_end_date)
                    exp2_companies.append(experience['company'])
                    exp2_company_urls.append(experience['company_linkedin_profile_url'])
                    exp2_titles.append(experience['title'])
                elif counter == 3: #If index is 2
                    try:
                        start_date = experience['starts_at']
                        exp3_start_date = self.date_parse(start_date)
                    except:
                        exp3_start_date = 'NULL'

                    try:
                        end_date = experience['ends_at']
                        exp3_end_date = self.date_parse(end_date)

                    except:
                        if exp3_start_date != 'NULL':
                            exp3_end_date = 'Present'
                        else:
                            exp3_end_date = 'NULL'
                    
                    exp3_start_dates.append(exp3_start_date)
                    exp3_end_dates.append(exp3_end_date)
                    exp3_companies.append(experience['company'])
                    exp3_company_urls.append(experience['company_linkedin_profile_url'])
                    exp3_titles.append(experience['title'])
                elif counter == 4: #If index is 3
                    try:
                        start_date = experience['starts_at']
                        exp4_start_date = self.date_parse(start_date)
                    except:
                        exp4_start_date = 'NULL'

                    try:
                        end_date = experience['ends_at']
                        exp4_end_date = self.date_parse(end_date)

                    except:
                        if exp4_start_date != 'NULL':
                            exp4_end_date = 'Present'
                        else:
                            exp4_end_date = 'NULL'
                    
                    exp4_start_dates.append(exp4_start_date)
                    exp4_end_dates.append(exp4_end_date)
                    exp4_companies.append(experience['company'])
                    exp4_company_urls.append(experience['company_linkedin_profile_url'])
                    exp4_titles.append(experience['title'])                              
                elif counter == 5: #If index is 4
                    try:
                        start_date = experience['starts_at']
                        exp5_start_date = self.date_parse(start_date)
                    except:
                        exp5_start_date = 'NULL'

                    try:
                        end_date = experience['ends_at']
                        exp5_end_date = self.date_parse(end_date)

                    except:
                        if exp5_start_date != 'NULL':
                            exp5_end_date = 'Present'
                        else:
                            exp5_end_date = 'NULL'
                    exp5_start_dates.append(exp5_start_date)
                    exp5_end_dates.append(exp5_end_date)
                    exp5_companies.append(experience['company'])
                    exp5_company_urls.append(experience['company_linkedin_profile_url'])
                    exp5_titles.append(experience['title'])
                else:
                    pass
        
        except ValueError:
            print("Incorrect value input.")
            exp1_start_dates.append('NULL - err')
            exp1_end_dates.append('NULL - err')
            exp1_companies.append('NULL - err')
            exp1_company_urls.append('NULL - err')
            exp1_titles.append('NULL - err')
            exp2_start_dates.append('NULL - err')
            exp2_end_dates.append('NULL - err')
            exp2_companies.append('NULL - err')
            exp2_company_urls.append('NULL - err')
            exp2_titles.append('NULL - err')
            exp3_start_dates.append('NULL - err')
            exp3_end_dates.append('NULL - err')
            exp3_companies.append('NULL - err')
            exp3_company_urls.append('NULL - err')
            exp3_titles.append('NULL - err')
            exp4_start_dates.append('NULL - err')
            exp4_end_dates.append('NULL - err')
            exp4_companies.append('NULL - err')
            exp4_company_urls.append('NULL - err')
            exp4_titles.append('NULL - err')
            exp5_start_dates.append('NULL - err')
            exp5_end_dates.append('NULL - err')
            exp5_companies.append('NULL - err')
            exp5_company_urls.append('NULL - err')
            exp5_titles.append('NULL - err')
            pass
        except IndexError:
            print("Index Not Found.")
            exp1_start_dates.append('NULL - err')
            exp1_end_dates.append('NULL - err')
            exp1_companies.append('NULL - err')
            exp1_company_urls.append('NULL - err')
            exp1_titles.append('NULL - err')
            exp2_start_dates.append('NULL - err')
            exp2_end_dates.append('NULL - err')
            exp2_companies.append('NULL - err')
            exp2_company_urls.append('NULL - err')
            exp2_titles.append('NULL - err')
            exp3_start_dates.append('NULL - err')
            exp3_end_dates.append('NULL - err')
            exp3_companies.append('NULL - err')
            exp3_company_urls.append('NULL - err')
            exp3_titles.append('NULL - err')
            exp4_start_dates.append('NULL - err')
            exp4_end_dates.append('NULL - err')
            exp4_companies.append('NULL - err')
            exp4_company_urls.append('NULL - err')
            exp4_titles.append('NULL - err')
            exp5_start_dates.append('NULL - err')
            exp5_end_dates.append('NULL - err')
            exp5_companies.append('NULL - err')
            exp5_company_urls.append('NULL - err')
            exp5_titles.append('NULL - err')
            pass
        
    def error_check_curl(self, response):
        #Check ProxyCurl errors
        if '400' in response: #If 400 error returned
            message = 'Invalid parameters provided. Refer to the documentation and message body for more info.' #Tell us
        elif '401' in response: #If 401 error returned
            message = 'Invalid API Key. Please check.' 
            pass
        elif '403' in response: #If 403 error returned
            message = 'No more credits. Please buy more.'
            pass
        elif '404' in response: #If 404 error returned
            message = 'Invalid source URL. Please check.'
            pass
        elif '429' in response: #If 429 error returned
            message = 'Rate limit has been exceeded. Please try again.'
            pass
        elif '500' in response: #If 500 error returned
            message = 'API error. Please contact Proxycurl/Nubela'
            pass
        elif '503' in response: #If 503 error returned
            message = 'Enrichment failed, please retry.'
        else: #If no error returned
            message = 'Connected.'  
        print(message)

    def error_check_google(self, code):
        if '400' in code: #If 400 error returned
            message = 'Bad Company Search Request.' #Tell us
        elif '401' in code: #If 401 error returned
            message = 'Invalid API Key. Please check.'
            pass
        elif '402' in code: #If 403 error returned
            message = 'Company search daily limit was exceeded. Please purchase credits.'
            pass
        elif '404' in code: #If 404 error returned
            message = 'Request not found. Please check search parameters.'
            pass
        elif '405' in code: #If 429 error returned
            message = 'HTTP method not allowed.'
            pass
        elif '410' in code: #If 500 error returned
            message = 'Request resource has been deleted. Please check.'
            pass
        elif '413' in code: #If 503 error returned
            message = 'Request to company API is too large. Please check parameters.'
        elif '416' in code:
            message = 'Cannot satisfy requested range in company API. Please check parameters.'
        elif '417' in code:
            message = 'Company API cannot fulfil request. Please check parameters.'
        elif '418' in code:
            message = 'Company API precondition not met. Please add If-Match or If-None-Match header to request.'
        elif '429' in code:
            message = 'Too many requests sent in a short time span. Please wait and start again.'
        elif '501' in code:
            message = 'Company API operation not implemented.'
        elif '503' in code:
            message = 'Company API Back End Error. Please try again.'
        else: #If no error returned
            message = 'Connected.'
        print(message)
    
    def export_error_file(self):
        print("Creating Error File")
        try:
            output_type = "error"
            #Define dictionary
            data = {
                #'I4B GUID':i4b_guid,
                'Error':error_code,
                'Link':error_link
                }
            export_filename = self.output_filename + '_ERROR_FILE'
            #Create Dataframe
            df = pd.DataFrame.from_dict(data)
            print("Creating Error File DataFrame")
            #Export Dataframe
            print("Exporting Error File")
            self.export_file(df, output_type)
        except ValueError:
            print("Incorrect value input " + str(err))
    
    def export_main_file(self):
        print("Creating output file.")
        #Define dictionary
        try:
            output_type = "main"            
            data = {
                "First Name": first_names,
                "Last Name": last_names,
                "Profile URL": profile_url,
                "Company Searched": company_looked_at,
                #"Gender": genders,
                #"Country": countries,
                #"Activity": activities,
                #"I4B Company": i4b_companies,
                #"I4B Company GUID": i4b_company_guids,
                #"I4B Company Country": i4b_company_countries,
                "Exp 1 Start Date": exp1_start_dates,
                "Exp 1 End Date": exp1_end_dates,
                "Exp 1 Company": exp1_companies,
                "Exp 1 Company URL": exp1_company_urls,
                "Exp 1 Title": exp1_titles,
                "Exp 2 Start Date": exp2_start_dates,
                "Exp 2 End Date": exp2_end_dates,
                "Exp 2 Company": exp2_companies,
                "Exp 2 Company URL": exp2_company_urls,
                "Exp 2 Title": exp2_titles,
                "Exp 3 Start Date": exp3_start_dates,
                "Exp 3 End Date": exp3_end_dates,
                "Exp 3 Company": exp3_companies,
                "Exp 3 Company URL": exp3_company_urls,
                "Exp 3 Title": exp3_titles,
                "Exp 4 Start Date": exp4_start_dates,
                "Exp 4 End Date": exp4_end_dates,
                "Exp 4 Company": exp4_companies,
                "Exp 4 Company URL": exp4_company_urls,
                "Exp 4 Title": exp4_titles,
                "Exp 5 Start Date": exp5_start_dates,
                "Exp 5 End Date": exp5_end_dates,
                "Exp 5 Company": exp5_companies,
                "Exp 5 Company URL": exp5_company_urls,
                "Exp 5 Title": exp5_titles,
            }
            print( #Print number of dictionary items for each key in the dictionary. Unecessary. Checks for inconsistent record values.
                "First Name" + str(len(first_names)), 
                "Last Name" + str(len(last_names)), 
                "Profile URL" + str(len(profile_url)), 
                "exp 1 start" + str(len(exp1_start_dates)), 
                "exp 1 end" + str(len(exp1_end_dates)), 
                "exp 1 url" + str(len(exp1_company_urls)), 
                "exp 1 company" + str(len(exp1_companies)),
                "exp 1 title" + str(len(exp1_titles)),
                "exp 2 start" + str(len(exp2_start_dates)),
                "exp 2 end" + str(len(exp2_end_dates)),
                "exp 2 url" + str(len(exp2_company_urls)),
                "exp 2 company" + str(len(exp2_companies)),
                "exp 2 title" + str(len(exp2_titles)),
                "exp 3 start " + str(len(exp3_start_dates)),
                "exp 3 end" + str(len(exp3_end_dates)),
                "exp 3 url" + str(len(exp3_company_urls)),
                "exp 3 company" + str(len(exp3_companies)),
                "exp 3 title" + str(len(exp3_titles)),
                "exp 4 start" + str(len(exp4_start_dates)),
                "exp 4 end" + str(len(exp4_end_dates)),
                "exp 4 company" + str(len(exp4_companies)),
                "exp 4 title" + str(len(exp4_titles)),
                "exp 5 start" + str(len(exp5_start_dates)),
                "exp 5 end" + str(len(exp5_end_dates)),
                "exp 5 url" + str(len(exp5_company_urls)),
                "exp 5 company" + str(len(exp5_companies)),
                "exp 5 title" + str(len(exp5_titles))
                )
            
            #Create Dataframe
            print("Creating output dataframe.")
            df = pd.DataFrame.from_dict(data)
            #Export Dataframe
            print("Exporting file.")
            self.export_file(df, output_type)
        except ValueError as err:
            print("Incorrect value input " + str(err))
        
    def export_file(self, df, output_type):
        try:
            #Get datetime as string
            date_string = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            if output_type == "main":
                #Create full output filename, using output_filename and date
                full_filename = f'{self.output_filename}_{date_string}.csv'
            elif output_type == "error":
                #Create full output filename, using output_filename and date
                full_filename = f'{self.output_filename}_ERROR_{date_string}.csv'
                #Export to .csv
            df.to_csv(f'{self.output_filepath}\{full_filename}', encoding='UTF-8')
            print(full_filename + " exported successfully.")
        except UnicodeEncodeError as err:
            print("Failed to encode file " + err)
        except ValueError as err:
            print("Incorrect value input. " + err)
            print("Export terminated.")
        except FileExistsError as err:
            print("File Named:" + full_filename + " Already Exists " + err)
        except PermissionError as err:
            print("You do not have permission to save file:" + full_filename + " please check." + err)
        except UnicodeWarning as err:
            print("Unicode Warning:" + err)
