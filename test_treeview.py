"""Simple test to verify Treeview works correctly."""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview Test")
root.geometry("800x400")

# Create a frame
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create scrollbar
scroll = ttk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Create treeview with headings only (no tree column)
tree = ttk.Treeview(frame,
                    columns=('Label', 'Name', 'Description', 'Required', 'TRL'),
                    show='headings',
                    yscrollcommand=scroll.set)
scroll.config(command=tree.yview)

# Set up columns
tree.heading('Label', text='Label')
tree.heading('Name', text='Name')
tree.heading('Description', text='Description')
tree.heading('Required', text='Required')
tree.heading('TRL', text='TRL Achieved')

tree.column('Label', width=120)
tree.column('Name', width=200)
tree.column('Description', width=300)
tree.column('Required', width=80)
tree.column('TRL', width=100)

tree.pack(fill=tk.BOTH, expand=True)

# Add some test data
tree.insert('', tk.END, values=('PF-1', 'Test Feature 1', 'This is a test description', 'Yes', 'TRL 6'))
tree.insert('', tk.END, values=('PF-2', 'Test Feature 2', 'Another description here', 'No', 'TRL 3'))
tree.insert('', tk.END, values=('PF-3', 'Test Feature 3', 'Yet another description', 'Yes', 'TRL 9'))

print(f"Tree has {len(tree.get_children())} items")

# Add a button to add more items
def add_item():
    import random
    num = random.randint(1, 100)
    tree.insert('', tk.END, values=(f'PF-{num}', f'Test {num}', f'Description {num}', 'Yes', 'TRL 6'))
    print(f"Added item. Tree now has {len(tree.get_children())} items")

btn = ttk.Button(root, text="Add Item", command=add_item)
btn.pack(pady=5)

root.mainloop()
