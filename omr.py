import utilis
import scan
import pandas as pd
import os
import datetime

current_time = datetime.datetime.now()


def omr(csv_path, images):
    # Define the expected headers
    expected_headers = ['Last Name', 'First Name', 'Middle Initial', 'ID', 'Exam ID', 'Answer Key']

    csv_folder_path = csv_path

    try:
        # Attempt to load the CSV file into a DataFrame
        df = pd.read_csv(csv_folder_path, dtype={'ID': str, 'Exam ID': str, 'Answer Key': str})
        
        # Check if the actual headers match the expected headers
        if list(df.columns) != expected_headers:
            raise ValueError(f"Error: CSV headers do not match the expected headers: {expected_headers}")
        
        # Display the first few rows of the DataFrame
        print("CSV file loaded successfully with correct headers.")

        # Create a dictionary to map IDs to personal information
        id_to_info = {
            row['ID']: {
                'Last Name': row['Last Name'],
                'First Name': row['First Name'],
                'Middle Initial': row['Middle Initial'],
                'Exam ID': row['Exam ID'],
                'Answer Key': row['Answer Key']
            }
            for _, row in df.iterrows()
        }

        image_folder_path = images
        last_folder = os.path.basename(image_folder_path)
        print(last_folder)
        image_file_paths = []

        try:
            if image_folder_path:
                image_files = utilis.get_image_files(image_folder_path)
                
                if image_files:
                    print("Found image files:")
                    for file in image_files:
                        # print(file)
                        image_file_paths.append(file)
                else:
                    raise Exception("No image files found in the specified folder.")
            else:
                raise Exception("No folder was selected.")
            
            print(image_file_paths)
            
            image_paths = image_file_paths

            filename = (f"Results_{last_folder}")
            filename = f"Results_{last_folder}_" + current_time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
            # content = ("Last Name,First Name,Middle Initial,ID,Score,Invalid Answer,Incorrect Answer")
            utilis.create_csv(filename)

            if len(image_paths) != len(id_to_info):
                print("Error: Lists of image paths, IDs, Exam IDs, and answer keys must have the same length.")
            else:
                for image_path in image_paths:
                    cropStud, cropExam, cropAns = scan.rect_locator(image_path)
                    id_marks = scan.id_scan(cropStud)
                    stud_id = scan.id_check(id_marks)
                    stud_id = utilis.int_list_to_string(stud_id)

                    if stud_id in id_to_info:
                        id_info = id_to_info[stud_id]
                        print(f"Image Path: {image_path}")
                        print(f"Exam ID: {id_info['Exam ID']}")
                        print(f"Answer Key: {id_info['Answer Key']}")
                    else:
                        raise ValueError(f"Error: Wrong student ID {stud_id}. ID not found in id_to_info dictionary.")
                    
                    exam_id_marks = scan.exam_id_scan(cropExam)
                    exam_id = scan.exam_id_check(exam_id_marks)
                    exam_id = utilis.int_list_to_string(exam_id)

                    exam_id_valid = utilis.are_strings_equal(id_info['Exam ID'], exam_id )

                    print(f"Processing file: {image_path} with ID: {stud_id}, Exam ID: {exam_id_valid}, and Answer Key: {id_info['Answer Key']}")
                    
                    answer_marks = scan.answer_scan(cropAns)
                    score, invAns, incAns = scan.ans_check(answer_marks, id_info['Answer Key'] )

                    print("Student ID:", stud_id)
                    print("Exam ID:", exam_id_valid)
                    print("Score:", score)
                    print("Invalid Answers:", invAns)
                    print("Incorrect Answers:", incAns)
        
                    additional_content = [ id_info['Last Name'],
                                            id_info['First Name'],
                                            id_info['Middle Initial'],
                                            stud_id,
                                            exam_id_valid,
                                            score,
                                            invAns,
                                            incAns
                                            ]
                    try:
                        utilis.append_to_csv(additional_content, filename)
                    except Exception as e:
                        print(f"Failed to append to text file: {e}")
                    
                    # except Exception as e:
                    #     print("An error occurred during processing:", str(e))

                    print("-" * 40)  # Separator for readability
                
            # utilis.txt_to_csv(filename, 'output.csv', image_folder_path, delimiter=' ')

        except Exception as e:
            print(e)
    except FileNotFoundError:
        print(f"Error: The file at '{csv_folder_path}' was not found. Please check the path.")

    except pd.errors.EmptyDataError:
        print("Error: The file is empty. Please provide a valid CSV file.")

    except pd.errors.ParserError:
        print("Error: There was an issue parsing the CSV file. Please check the file format.")

    except ValueError as ve:
        print(ve)

    except Exception as e:
            print(e)