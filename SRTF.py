from tkinter import *  #para magka roon ng GUI
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import heapq
class SRTF:

    def __init__(self, window):
        self.window = window
        self.window.geometry("1920x1024")
        self.window.title("SRTF")
        
        #dito input kung ilang jobs ilalagay
        self.process_label = tk.Label(window, text="Enter The number of Jobs you are going to Process: ", font=('Helvetica', 20), width=40, justify="center", bg="skyblue", fg="black")
        self.process_label.grid(row=0, column=0, padx=10, pady=5)
        self.process_entry = tk.Entry(window, highlightbackground="black", highlightthickness=1, width=30, justify="center", font=('Helvetica', 16) )  #ito yung input kung ilang numjobs
        self.process_entry.grid(row=0, column=1, padx=20, pady=10) 

        #the button that will change the table
        self.button = tk.Button(window, text="Update", command=self.update_table, width=10, font=('Helvetica', 14), anchor="center", bg="#F7E59D", fg="black")
        self.button.grid(row=0, column=2, padx=10, pady=5)


        self.process_list = []
        self.process_list_list = [] #dito naalagay yung mga ininput

        self.gantt_text = None
        self.completion_text = None
        self.timeline_canvas = None
        
        
        
    def update_table(self):
        try:
            num_jobs = int(self.process_entry.get())
            if num_jobs <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of jobs.")
            return
        self.input_frame = tk.Frame(self.window)
        self.input_frame.configure(bg="#D2F4F5")
        self.input_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')

        #pag nagupdate kung ilang job aalisin yung mga nainput nung una
        self.process_list.clear()
        self.process_list_list.clear()
        
        #dito yung mga input 
        job_title = tk.Label(self.input_frame, bg="skyblue", font=('Helvetica', 14), text="Job")
        job_title.grid(row=1, column = 1)
        AT_title = tk.Label(self.input_frame, bg="#F7E59D", font=('Helvetica', 14), text="Arrival time")
        AT_title.grid(row=1, column = 2)
        BT_title = tk.Label(self.input_frame, bg="skyblue", font=('Helvetica', 14), text="Burst Time")
        BT_title.grid(row=1, column = 3)
    

        for i in range(num_jobs):
            job_label = tk.Label(self.input_frame, highlightbackground="black", highlightthickness=1, font=('Helvetica', 14), text=f"Job {i+1}: ", width=5)
            job_label.grid(row=i+2, column=1)
            
            arrival_entry = tk.Entry(self.input_frame, highlightbackground="black", highlightthickness=1, justify="center", width=20, font=('Helvetica', 14))
            arrival_entry.grid(row=i+2, column=2)
            
            burst_entry = tk.Entry(self.input_frame, highlightbackground="black", highlightthickness=1, justify="center", width=20, font=('Helvetica', 14))
            burst_entry.grid(row=i+2, column=3)
            
            self.process_list.extend([ arrival_entry, burst_entry])
            self.process_list_list.append((arrival_entry, burst_entry))

        run_button = tk.Button(self.input_frame, text="Run SRTF", width=15, font=('Helvetica', 14), anchor="center", bg="#F7E59D", fg="black", command=self.Calculate_SRTF)
        run_button.grid(row=num_jobs+2, column = 0, columnspan=5)


    #dito icocompute tapos isosort yung algorithm
    def srtf(self, job_list):
        time = 0
        gantt = []
        timeline = []
        completed = {}
        job_list.sort(key=lambda x: x[0])
        job_queue = []
        original_burst_times = {job[2]: job[1] for job in job_list}

        i = 0
        current_job = None
        start_time = None

        while i < len(job_list) or job_queue:
            while i < len(job_list) and job_list[i][0] <= time:
                heapq.heappush(job_queue, (job_list[i][1], job_list[i][0], job_list[i][2]))
                i += 1

            if job_queue:
                burst_time, arrival_time, job_name = heapq.heappop(job_queue)
                if current_job != job_name:
                    if current_job is not None:
                        timeline.append((current_job, arrival_time, start_time, time))
                        gantt.append((current_job, start_time, time))
                    current_job = job_name
                    start_time = time
                burst_time -= 1
                time += 1

                if burst_time > 0:
                    heapq.heappush(job_queue, (burst_time, arrival_time, job_name))
                else:
                    ct = time
                    tat = ct - arrival_time
                    wt = tat - original_burst_times[job_name]
                    completed[job_name] = [arrival_time, original_burst_times[job_name], ct, tat, wt]
            else:
                time += 1

        if current_job is not None:
            timeline.append((current_job, arrival_time, start_time, ct))
            gantt.append((current_job, start_time, time))

        return gantt, completed, timeline

    def average(self, completed):
        num_jobs = int(self.process_entry.get())
        total_tat = sum(values[3] for values in completed.values())
        average_tat = total_tat / num_jobs

        total_wt = sum(values[4]for values in completed.values())
        average_wt = total_wt / num_jobs

        return average_tat, average_wt

    def average(self, completed):
        num_jobs = int(self.process_entry.get())
        total_tat = sum(values[3] for values in completed.values())
        average_tat = total_tat / num_jobs

        total_wt = sum(values[4]for values in completed.values())
        average_wt = total_wt / num_jobs

        return average_tat, average_wt
    
    
    def Calculate_SRTF(self):
        try:
            #gagawa bagong window
            solution_window = tk.Toplevel(self.window)
            solution_window.title("SOLUTION")
            solution_window.geometry("1920x1080")
            #Ito yung paglalagyan ng result
            self.gantt_text = tk.Text(solution_window, height=8, width=200)  
            self.gantt_text.grid(row=2, column = 0, columnspan=5) 
            self.gantt_text.config(state=tk.DISABLED)  

            self.completion_text = tk.Text(solution_window, height=10, width=200) 
            self.completion_text.grid(row=1, columnspan=5) 
            self.completion_text.config(state=tk.DISABLED) 

            self.timeline_canvas = tk.Canvas(solution_window, bg='white', height=370, width=1350)
            self.timeline_canvas.grid(row=3, column=0, pady=0, columnspan=2)

            # Horizontal scrollbar for timeline canvas
            self.timeline_scrollbar_x = tk.Scrollbar(solution_window, orient=tk.HORIZONTAL, command=self.timeline_canvas.xview)
            self.timeline_scrollbar_x.grid(row=4, column=0, sticky=tk.EW, columnspan=2)
            
            # Vertical scrollbar for timeline canvas
            self.timeline_scrollbar_y = tk.Scrollbar(solution_window, orient=tk.VERTICAL, command=self.timeline_canvas.yview)
            self.timeline_scrollbar_y.grid(row=3, column=2, sticky=tk.NS)
            # Configure canvas to use both scrollbars
            self.timeline_canvas.configure(xscrollcommand=self.timeline_scrollbar_x.set, yscrollcommand=self.timeline_scrollbar_y.set)

            process_list = []
            for arrival_entry, burst_entry in self.process_list_list:
                arrival_time = int(arrival_entry.get())
                burst_time = int(burst_entry.get())
                process_list.append([arrival_time, burst_time, f"p{len(process_list) + 1}"])
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for arrival and burst times.")
            return

        gantt, completed, timeline = self.srtf(process_list)
        average_tat, average_wt = self.average(completed)

        process = len(process_list)
        # ito yung sa gantt chart
        self.gantt_text.config(state=tk.NORMAL)
        self.gantt_text.delete(1.0, tk.END)
        self.gantt_text.insert(tk.END, "Gantt Chart:\n")
        for task, arrival_time, ct in gantt:
            self.gantt_text.insert(tk.END, f"{' '* 5} |{task}|")
        self.gantt_text.insert(tk.END, "\n")
        for task, arrival_time, ct in gantt:
            self.gantt_text.insert(tk.END, f"{' '* 6} ({ct})")
        self.gantt_text.insert(tk.END, "\n\n")
        self.gantt_text.insert(tk.END, "Timeline:\n")
        self.gantt_text.insert(tk.END, f"{'-------+' *  (process+1)}")
        self.gantt_text.insert(tk.END, "\n")
        for task, arrival_time, start_time, ct in timeline:
            self.gantt_text.insert(tk.END, f"{' ' * 4} {arrival_time}{' ' * 3}||")
        self.gantt_text.insert(tk.END, "\n")
        for task, arrival_time, start_time, ct in timeline:
            self.gantt_text.insert(tk.END, f"{' ' * 2}{task}({ct}){' ' * 2}")
                
        
        self.gantt_text.insert(tk.END, "\n")
       

        #ito yung sa table
        self.completion_text.config(state=tk.NORMAL)
        self.completion_text.delete(1.0, tk.END)
        self.completion_text.insert(END, "Table:\n")
        self.completion_text.insert(END, f"||   JOB   ||   Arrival Time   ||   Burst Time   ||   Completion Time   ||   Turn Around Time   ||   Waiting Time   ||\n")
        for pid, values in completed.items():
            self.completion_text.insert(END, f"{' ' * 6}{pid}{' ' * 13}{values[0]}{' ' * 16}{values[1]}{' ' * 18}{values[2]}{' ' * 24}{values[3]}{' ' * 24}{values[4]}{' ' * 10}\n")
        self.completion_text.insert(tk.END,"\n")
        self.completion_text.insert(tk.END, "Average:\n")
        self.completion_text.insert(tk.END, f"Turn Around Time: {average_tat: .2f} \n")
        self.completion_text.insert(tk.END, f"Waiting TIme: {average_wt: .2f} \n")
        self.completion_text.config(state=tk.DISABLED)  # Disable text widget after insertion  

        #ito naman sa timeline
        max_completion_time = max(process[2] for process in completed.values())
        scale = 20  # Adjust scale for timeline

        # Draw horizontal line for timeline
        self.timeline_canvas.create_line(50, 50, max_completion_time * scale + 50, 50, width=2)  # fix

        for task, arrival_time, start_time, ct in timeline:
            start_x = max(arrival_time, 0) * scale + 50
            end_x = ct * scale + 50
            y = 80 + 30 * int(task[1:])

            # Draw process burst time bar
            self.timeline_canvas.create_rectangle(start_x, y - 10, end_x, y + 10, fill='skyblue')

            # Draw labels for process
            self.timeline_canvas.create_text((start_x + end_x) // 2, y, anchor='center', text=task, font=('Arial', 10))
            self.timeline_canvas.create_text(start_x, y + 20, anchor='center', text=str(arrival_time), font=('Arial', 10))
            self.timeline_canvas.create_text(end_x, y + 20, anchor='center', text=str(ct), font=('Arial', 10))


            #para sa scroll ng canvas    
            self.timeline_canvas.update_idletasks()
            self.timeline_canvas.config(scrollregion=self.timeline_canvas.bbox("all"))
            