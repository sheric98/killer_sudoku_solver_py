import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Widget

from src.constants import MAX_NUMBER, SQUARES_KEY, SUM_KEY
from src.solver_executor import solve_from_arr


class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.cell_len = 50
		grid_len = self.cell_len * MAX_NUMBER
		x_padding = 500
		y_padding = 200
		self.x_grid_padding = 25
		self.y_grid_padding = y_padding - 25
		self.mouse_down = False

		self.curr = None

		self.bind('<ButtonPress-1>', self._mouse_down)
		self.bind('<ButtonRelease-1>', self._mouse_up)
		self.bind('<Return>', lambda e: self._try_submit_group())
		self.geometry(f"{grid_len + x_padding}x{grid_len + y_padding}")
		self.canvas = tk.Canvas(self, width=grid_len, height=grid_len, borderwidth=0, highlightthickness=0)
		self.canvas.pack(side="top", fill="both", expand="true")
		self.canvas.place(relx=0, rely=0, x=self.x_grid_padding, y=self.y_grid_padding, anchor=tk.NW)

		self.solve_status = ttk.Label(self, text='')
		self.solve_status.place(relx=0, rely=0, x=self.x_grid_padding + grid_len // 2, y=100, anchor=tk.CENTER)

		self.input_var = tk.StringVar(self)
		
		self.submit_status = ttk.Label(self, text='')
		self.submit_status.place(relx=1, rely=0.5, x=-(x_padding // 2), y=-100, anchor=tk.CENTER)

		self.input_label = ttk.Label(self, text="Group sum:")
		self.input_label.place(relx=1, rely=0.5, x=-(x_padding // 2) - 140, y=-50, anchor=tk.CENTER)
		self.input = ttk.Entry(self, textvariable=self.input_var)
		self.input.place(relx=1, rely=0.5, x=-(x_padding // 2), y=-50, anchor=tk.CENTER)
		self.input.focus_set()

		self.group_button = ttk.Button(self, text="Create Group", command=self._try_submit_group)
		self.group_button.place(relx=1, rely=0.5, x=-(x_padding // 2), y=0, anchor=tk.CENTER)

		self.solve_button = ttk.Button(self, text="Solve", command=self._solve)
		self.solve_button.place(relx=1, rely=0.5, x=-(x_padding // 2), y=50, anchor=tk.CENTER)

		self.rect = {}
		self.txts = {}
		self.selected = set()
		self.submitted = set()
		self.groups = []
		for column in range(MAX_NUMBER):
			for row in range(MAX_NUMBER):
				x1 = column*self.cell_len
				y1 = row * self.cell_len
				x2 = x1 + self.cell_len
				y2 = y1 + self.cell_len
				obj = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
				self.txts[column, row] = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, font=("Purisa", 20), text='')
				self.rect[column, row] = obj

		self.canvas.bind("<Leave>", self._grid_leave)
		self.bind('<B1-Motion>', self._motion)

	def _motion(self, e):
		if e.widget.winfo_containing(e.x_root, e.y_root) == self.canvas:
			if e.widget == self.canvas:
				x = e.x
				y = e.y
			else:
				x = e.x - self.x_grid_padding
				y = e.y - self.y_grid_padding
			col = x // self.cell_len
			row = y // self.cell_len

			if (col, row) != self.curr:
				self.curr = (col, row)
				self._update_square(col, row)

	def _mouse_down(self, e):
		self.mouse_down = True
		# if self.curr is not None:
		# 	self._update_square(*self.curr)

	def _mouse_up(self, e):
		self.mouse_down = False

	def _add_text(self, txt, col, row):
		self.canvas.itemconfig(self.txts[col, row], text=txt)

	def _solve(self):
		res = solve_from_arr(self.groups)
		
		if len(res) == 1:
			self.canvas.itemconfig("rect", fill="white")
			self.solve_status.config(text="Solution:")
			self._display_board(res[0])
		elif len(res) > 1:
			self.canvas.itemconfig("rect", fill="blue")
			self.solve_status.config(text=f"{len(res)} solutions found. Here is one:")
			self._display_board(res[0])
		else:
			self.canvas.itemconfig("rect", fill="red")
			self.solve_status.config(text="No solutions found.")
		
	def _display_board(self, board):
		for r, row in enumerate(board):
			for c, num in enumerate(row):
				self._add_text(str(num), c, r)

	def _try_submit_group(self):
		self.submit_status.config(text='')
		inp = self.input_var.get()
		self.input.focus_set()
		try:
			num = int(inp)
		except Exception:
			self.submit_status.config(text='Group sum must be a number')
			return
		
		if not self.selected:
			self.submit_status.config(text="Must select at least one square")
			return

		self._submit_group(num)
		self.input.delete(0, 'end')

	def _submit_group(self, num):
		group_objs = []
		for k in self.selected:
			self.canvas.itemconfig(self.rect[k], fill="gray")
			self.submitted.add(k)
			col, row = k
			group_objs.append([row, col])
		self.selected.clear()
		self.groups.append({SUM_KEY: num, SQUARES_KEY: group_objs})

	def _grid_leave(self, e):
		self.curr = None

	def _update_square(self, col, row):
		k = (col, row)
		if k in self.submitted:
			return
		elif k in self.selected:
			self.canvas.itemconfig(self.rect[k], fill="white")
			self.selected.remove(k)
		else:
			self.canvas.itemconfig(self.rect[k], fill="green")
			self.selected.add(k)		

if __name__ == "__main__":
    app = App()
    app.mainloop()