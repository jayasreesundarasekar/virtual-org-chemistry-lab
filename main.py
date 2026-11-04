"""
COSMIC MOLECULE LAB — Pure Python desktop edition
Requires: Python 3.10+, rdkit
Optional online compound lookup: requests
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math, threading, urllib.parse, json

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem, Draw
    from PIL import Image, ImageTk
    RDKIT_OK=True
except Exception:
    RDKIT_OK=False

try:
    import requests
except Exception:
    requests=None

MOLECULES = ['Methane', 'Ethane', 'Propane', 'Butane', 'Pentane', 'Hexane', 'Heptane', 'Octane', 'Nonane', 'Decane', 'Ethene', 'Propene', '1-Butene', '1-Pentene', '1-Hexene', 'Ethylene glycol', 'Propylene glycol', 'Ethanol', 'Methanol', '1-Propanol', '2-Propanol', '1-Butanol', '2-Butanol', 'tert-Butanol', '1-Pentanol', '1-Hexanol', '1-Heptanol', '1-Octanol', 'Glycerol', 'Cyclohexanol', 'Benzyl alcohol', 'Phenol', 'Catechol', 'Resorcinol', 'Hydroquinone', '1-Naphthol', '2-Naphthol', 'Formaldehyde', 'Acetaldehyde', 'Propanal', 'Butanal', 'Benzaldehyde', 'Acetone', '2-Butanone', '2-Pentanone', 'Cyclohexanone', 'Acetophenone', 'Benzophenone', 'Formic acid', 'Acetic acid', 'Propionic acid', 'Butyric acid', 'Valeric acid', 'Caproic acid', 'Oxalic acid', 'Malonic acid', 'Succinic acid', 'Glutaric acid', 'Adipic acid', 'Benzoic acid', 'Salicylic acid', 'Cinnamic acid', 'Lactic acid', 'Citric acid', 'Tartaric acid', 'Malic acid', 'Oleic acid', 'Stearic acid', 'Palmitic acid', 'Acrylic acid', 'Methacrylic acid', 'Fumaric acid', 'Maleic acid', 'Glycine', 'Alanine', 'Valine', 'Leucine', 'Isoleucine', 'Serine', 'Threonine', 'Cysteine', 'Methionine', 'Aspartic acid', 'Glutamic acid', 'Asparagine', 'Glutamine', 'Lysine', 'Arginine', 'Histidine', 'Phenylalanine', 'Tyrosine', 'Tryptophan', 'Proline', 'Hydroxyproline', 'Urea', 'Thiourea', 'Acetamide', 'Formamide', 'Benzamide', 'N,N-Dimethylformamide', 'Acetonitrile', 'Propionitrile', 'Benzonitrile', 'Nitromethane', 'Nitrobenzene', 'Aniline', 'Toluidine', 'N,N-Dimethylaniline', 'Pyridine', 'Pyrrole', 'Furan', 'Thiophene', 'Imidazole', 'Pyrazole', 'Pyrimidine', 'Purine', 'Indole', 'Quinoline', 'Isoquinoline', 'Piperidine', 'Piperazine', 'Morpholine', 'Anisole', 'Phenetole', 'Diphenyl ether', 'Benzene', 'Toluene', 'Ethylbenzene', 'Styrene', 'o-Xylene', 'm-Xylene', 'p-Xylene', 'Cumene', 'Mesitylene', 'Naphthalene', 'Anthracene', 'Phenanthrene', 'Biphenyl', 'Fluorene', 'Fluoranthene', 'Pyrene', 'Benzyl chloride', 'Chloroform', 'Dichloromethane', 'Carbon tetrachloride', 'Chlorobenzene', 'Bromobenzene', 'Iodobenzene', 'Vinyl chloride', '1,2-Dichloroethane', 'Trichloroethylene', 'Tetrachloroethylene', 'Ethyl acetate', 'Methyl acetate', 'Propyl acetate', 'Butyl acetate', 'Isoamyl acetate', 'Methyl benzoate', 'Ethyl benzoate', 'Dimethyl carbonate', 'Diethyl carbonate', 'Ethyl formate', 'Methyl butyrate', 'Methyl salicylate', 'Lactone', 'Diethyl ether', 'Dimethyl ether', 'Tetrahydrofuran', '1,4-Dioxane', 'Dibutyl ether', 'Acetic anhydride', 'Phthalic anhydride', 'Maleic anhydride', 'Benzylamine', 'Ethylamine', 'Diethylamine', 'Triethylamine', 'Methylamine', 'Dimethylamine', 'Trimethylamine', 'Ethanolamine', 'Triethanolamine', 'Acetamidine', 'Guanidine', 'Hexamethylenetetramine', 'Glucose', 'Fructose', 'Galactose', 'Ribose', 'Deoxyribose', 'Sucrose', 'Lactose', 'Maltose', 'Cellobiose', 'Starch repeat unit', 'Cellulose repeat unit', 'Ascorbic acid', 'Dehydroascorbic acid', 'Caffeine', 'Theobromine', 'Theophylline', 'Aspirin', 'Paracetamol', 'Ibuprofen', 'Naproxen', 'Diclofenac', 'Ketoprofen', 'Lidocaine', 'Benzocaine', 'Procaine', 'Menthol', 'Camphor', 'Vanillin', 'Eugenol', 'Limonene', 'Citral', 'Geraniol', 'Linalool', 'Menthone', 'Thymol', 'Carvacrol', 'Cinnamaldehyde', 'Coumarin', 'Quercetin', 'Resveratrol', 'Curcumin', 'Cholesterol', 'Testosterone', 'Estradiol', 'Progesterone', 'Cortisol', 'Uric acid', 'Creatinine', 'Nicotinamide', 'Nicotinic acid', 'Pyridoxine', 'Thiamine', 'Riboflavin', 'Biotin', 'Folic acid', 'Retinol', 'Tocopherol', 'Coenzyme Q10', 'Melatonin', 'Dopamine', 'Serotonin', 'Adrenaline', 'Noradrenaline', 'Histamine', 'Acetylcholine']

EXAMPLES = {
    "Water": "O", "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O", "Benzene": "c1ccccc1",
    "Ethanol": "CCO", "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O"
}
COLORS={"C":"#a58bff","O":"#ff6b8d","N":"#6eeaff","H":"#e2e9ff","S":"#f4d35e","F":"#80ed99","Cl":"#80ed99","Br":"#d98c5f","P":"#ffb86b"}

class CosmicLab:
    def __init__(self, root):
        self.root=root
        root.title("COSMIC MOLECULE LAB | Python Edition")
        root.geometry("1220x820")
        root.minsize(900,650)
        self.bg="#090914"; self.panel="#121222"; self.panel2="#19192d"
        self.fg="#f4efff"; self.muted="#aaa4c5"; self.pink="#ff6b9d"; self.cyan="#6eeaff"
        root.configure(bg=self.bg)
        self.current=None; self.current_smiles=""; self.current_name=""; self.canonical=""
        self.rot_x=-.25; self.rot_y=.35; self.zoom=1.0; self.auto_spin=True; self.drag=None
        self._build()
        self.root.after(35,self._animate)
        if not RDKIT_OK:
            self.status.set("RDKit is not installed. Run: pip install rdkit pillow")
        else:
            self.status.set("Local RDKit chemistry engine ready.")

    def _build(self):
        style=ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",background=self.bg,borderwidth=0)
        style.configure("TNotebook.Tab",background=self.panel2,foreground=self.fg,padding=(18,10),font=("Segoe UI",10,"bold"))
        style.map("TNotebook.Tab",background=[("selected","#30264a")],foreground=[("selected",self.cyan)])
        top=tk.Frame(self.root,bg=self.bg); top.pack(fill="x",padx=24,pady=(18,10))
        tk.Label(top,text="✦  COSMIC",fg=self.fg,bg=self.bg,font=("Segoe UI",23,"bold")).pack(side="left")
        tk.Label(top,text="MOLECULE LAB",fg=self.pink,bg=self.bg,font=("Segoe UI",23,"bold")).pack(side="left")
        tk.Label(top,text="  PYTHON DESKTOP EDITION",fg=self.muted,bg=self.bg,font=("Segoe UI",9,"bold")).pack(side="left",pady=(13,0))
        self.status=tk.StringVar()
        tk.Label(self.root,textvariable=self.status,anchor="w",bg="#10101d",fg=self.cyan,padx=24,pady=8,font=("Consolas",9)).pack(fill="x")
        self.tabs=ttk.Notebook(self.root); self.tabs.pack(fill="both",expand=True,padx=18,pady=15)
        self.lab=tk.Frame(self.tabs,bg=self.bg); self.tabs.add(self.lab,text="MOLECULAR LAB")
        self.library=tk.Frame(self.tabs,bg=self.bg); self.tabs.add(self.library,text="COMPOUND LIBRARY")
        self.learn=tk.Frame(self.tabs,bg=self.bg); self.tabs.add(self.learn,text="CHEMISTRY GUIDE")
        self.quiz=tk.Frame(self.tabs,bg=self.bg); self.tabs.add(self.quiz,text="QUEST / QUIZ")
        self._build_lab(); self._build_library(); self._build_learn(); self._build_quiz()
        self.load_smiles(EXAMPLES["Water"],"Water")

    def card(self,parent):
        return tk.Frame(parent,bg=self.panel,highlightbackground="#292541",highlightthickness=1)

    def _build_lab(self):
        left=self.card(self.lab); left.pack(side="left",fill="both",expand=True,padx=(0,10),pady=8)
        right=self.card(self.lab); right.pack(side="right",fill="y",padx=(10,0),pady=8)
        tk.Label(left,text="MOLECULAR CORE",bg=self.panel,fg=self.cyan,font=("Segoe UI",12,"bold")).pack(anchor="w",padx=18,pady=(16,3))
        self.mol_title=tk.Label(left,text="WATER  ·  H₂O",bg=self.panel,fg=self.fg,font=("Segoe UI",20,"bold")); self.mol_title.pack(anchor="w",padx=18)
        self.note=tk.Label(left,text="Drag to rotate • scroll to zoom • auto-spin",bg=self.panel,fg=self.muted,font=("Segoe UI",9)); self.note.pack(anchor="w",padx=18,pady=(2,10))
        self.viewer=tk.Canvas(left,bg="#080812",highlightthickness=0,height=390); self.viewer.pack(fill="both",expand=True,padx=14,pady=8)
        self.viewer.bind("<ButtonPress-1>",self._start_drag); self.viewer.bind("<B1-Motion>",self._drag); self.viewer.bind("<ButtonRelease-1>",lambda e:setattr(self,"drag",None)); self.viewer.bind("<MouseWheel>",self._wheel)
        controls=tk.Frame(left,bg=self.panel); controls.pack(fill="x",padx=16,pady=12)
        self._btn(controls,"⟳ AUTO SPIN: ON",self.toggle_spin).pack(side="left",padx=4)
        self._btn(controls,"RESET VIEW",self.reset_view).pack(side="left",padx=4)
        self._btn(controls,"2D STRUCTURE",self.show_2d).pack(side="left",padx=4)
        tk.Label(right,text="SMILES WORKSPACE",bg=self.panel,fg=self.pink,font=("Segoe UI",12,"bold")).pack(anchor="w",padx=16,pady=(16,8))
        tk.Label(right,text="Compound name or SMILES",bg=self.panel,fg=self.muted).pack(anchor="w",padx=16)
        self.name_entry=ttk.Entry(right,width=35); self.name_entry.pack(fill="x",padx=16,pady=(3,8))
        tk.Label(right,text="SMILES notation",bg=self.panel,fg=self.muted).pack(anchor="w",padx=16)
        self.smiles_entry=ttk.Entry(right,width=35); self.smiles_entry.pack(fill="x",padx=16,pady=(3,8))
        self._btn(right,"ANALYZE SMILES",self.analyze).pack(fill="x",padx=16,pady=4)
        self._btn(right,"LOOK UP COMPOUND ONLINE",self.lookup).pack(fill="x",padx=16,pady=4)
        self._btn(right,"LOAD ASPIRIN EXAMPLE",lambda:self.load_smiles(EXAMPLES["Aspirin"],"Aspirin")).pack(fill="x",padx=16,pady=4)
        self._btn(right,"COPY CANONICAL SMILES",self.copy_smiles).pack(fill="x",padx=16,pady=4)
        self._btn(right,"EXPORT TEXT REPORT",self.export_report).pack(fill="x",padx=16,pady=4)
        tk.Label(right,text="MOLECULAR PROPERTIES",bg=self.panel,fg=self.cyan,font=("Segoe UI",11,"bold")).pack(anchor="w",padx=16,pady=(17,6))
        self.props=tk.Text(right,width=39,height=14,bg="#0b0b17",fg=self.fg,insertbackground=self.fg,relief="flat",font=("Consolas",9),wrap="word")
        self.props.pack(fill="both",expand=True,padx=16,pady=(0,16)); self.props.configure(state="disabled")

    def _btn(self,parent,label,cmd):
        return tk.Button(parent,text=label,command=cmd,bg="#30264a",fg=self.fg,activebackground="#514071",activeforeground="white",relief="flat",bd=0,padx=10,pady=9,font=("Segoe UI",9,"bold"),cursor="hand2")

    def _build_library(self):
        head=tk.Frame(self.library,bg=self.bg); head.pack(fill="x",pady=12)
        tk.Label(head,text="250-COMPOUND ORGANIC LIBRARY",bg=self.bg,fg=self.fg,font=("Segoe UI",17,"bold")).pack(anchor="w")
        self.filter=tk.StringVar()
        entry=ttk.Entry(head,textvariable=self.filter); entry.pack(fill="x",pady=10)
        self.filter.trace_add("write",lambda *_:self.refresh_library())
        body=tk.Frame(self.library,bg=self.panel); body.pack(fill="both",expand=True)
        self.listbox=tk.Listbox(body,bg=self.panel,fg=self.fg,selectbackground="#514071",font=("Segoe UI",11),relief="flat",borderwidth=0)
        sb=ttk.Scrollbar(body,command=self.listbox.yview); self.listbox.configure(yscrollcommand=sb.set)
        self.listbox.pack(side="left",fill="both",expand=True,padx=10,pady=10); sb.pack(side="right",fill="y",pady=10)
        self.listbox.bind("<Double-Button-1>",self.pick_library)
        self.refresh_library()
        tk.Label(self.library,text="Double-click a compound to resolve its PubChem record. Internet access is needed for name lookup.",bg=self.bg,fg=self.muted).pack(anchor="w",pady=8)

    def refresh_library(self):
        if not hasattr(self,"listbox"): return
        q=self.filter.get().lower()
        self.filtered=[x for x in MOLECULES if q in x.lower()]
        self.listbox.delete(0,"end")
        for x in self.filtered:self.listbox.insert("end",x)
        self.status.set(f"Library filter: {len(self.filtered)} / 250 compounds")

    def pick_library(self,event=None):
        sel=self.listbox.curselection()
        if sel:self.name_entry.delete(0,"end"); self.name_entry.insert(0,self.filtered[sel[0]]); self.lookup()

    def _build_learn(self):
        box=self.card(self.learn); box.pack(fill="both",expand=True,padx=8,pady=8)
        content=[
            ("01  ATOMS & ELEMENTS","Atoms are the fundamental units of chemical elements. In molecular models, each element is represented by a symbol and often a distinct color."),
            ("02  CHEMICAL BONDS","Covalent bonds form when atoms share electron pairs. Single, double and triple bonds represent one, two and three shared pairs respectively."),
            ("03  READING SMILES","SMILES encodes molecular structures as text. Letters represent atoms, parentheses indicate branches, '=' and '#' indicate multiple bonds, and matching digits mark ring closures."),
            ("04  MOLECULAR DESCRIPTORS","Molecular formula counts atoms. Molecular weight estimates mass. LogP estimates partitioning between octanol and water. TPSA estimates polar surface area. H-bond donor/acceptor counts and rotatable bonds help describe molecular behaviour."),
            ("05  IMPORTANT NOTE","Computed descriptors are estimates, not experimental measurements. Confirm chemical identity and consult validated references before using values in academic or laboratory work.")
        ]
        for title,body in content:
            tk.Label(box,text=title,bg=self.panel,fg=self.cyan,font=("Segoe UI",13,"bold")).pack(anchor="w",padx=22,pady=(20,4))
            tk.Label(box,text=body,bg=self.panel,fg=self.fg,font=("Segoe UI",11),wraplength=1000,justify="left").pack(anchor="w",padx=22)

    def _build_quiz(self):
        box=self.card(self.quiz); box.pack(fill="both",expand=True,padx=8,pady=8)
        tk.Label(box,text="QUEST 001  /  DECODE THE STRUCTURE",bg=self.panel,fg=self.pink,font=("Segoe UI",17,"bold")).pack(anchor="w",padx=24,pady=(28,18))
        tk.Label(box,text="In SMILES notation, what do matching digits indicate?",bg=self.panel,fg=self.fg,font=("Segoe UI",14)).pack(anchor="w",padx=24,pady=8)
        self.feedback=tk.StringVar(value="Choose an answer to check your chemistry knowledge.")
        for label,correct in [("Ring closures",True),("Formal charges",False),("Atom isotopes",False),("Hydrogen counts",False)]:
            self._btn(box,label,lambda c=correct:self.feedback.set("Correct! Matching digits indicate ring closures in SMILES." if c else "Not quite. Matching digits indicate ring closures in SMILES.")).pack(anchor="w",padx=24,pady=5)
        tk.Label(box,textvariable=self.feedback,bg=self.panel,fg=self.cyan,font=("Segoe UI",11),wraplength=800).pack(anchor="w",padx=24,pady=18)

    def load_smiles(self,smiles,name="Custom molecule"):
        self.smiles_entry.delete(0,"end"); self.smiles_entry.insert(0,smiles)
        self.name_entry.delete(0,"end"); self.name_entry.insert(0,name)
        self._analyze(smiles,name)

    def analyze(self):
        self._analyze(self.smiles_entry.get().strip(),self.name_entry.get().strip() or "Custom molecule")

    def _analyze(self,smiles,name):
        if not RDKIT_OK:
            messagebox.showerror("RDKit required","Install dependencies with: pip install -r requirements.txt"); return
        mol=Chem.MolFromSmiles(smiles)
        if mol is None:
            messagebox.showerror("Invalid SMILES","RDKit could not parse this SMILES notation."); self.status.set("Invalid or unsupported SMILES."); return
        self.current=mol; self.current_smiles=smiles; self.current_name=name
        self.canonical=Chem.MolToSmiles(mol,canonical=True)
        self.smiles_entry.delete(0,"end"); self.smiles_entry.insert(0,smiles)
        self.mol_title.config(text=f"{name.upper()}  ·  {rdMolDescriptors.CalcMolFormula(mol)}")
        self._update_props()
        self.reset_view()
        self.status.set("Molecule analyzed locally with RDKit. 2D depiction and descriptors are ready.")

    def _update_props(self):
        m=self.current
        rows=[
            ("Molecular formula",rdMolDescriptors.CalcMolFormula(m)),
            ("Molecular weight",f"{Descriptors.MolWt(m):.3f} g/mol"),
            ("Exact mass",f"{Descriptors.ExactMolWt(m):.3f}"),
            ("LogP",f"{Descriptors.MolLogP(m):.3f}"),
            ("TPSA",f"{rdMolDescriptors.CalcTPSA(m):.3f} Å²"),
            ("H-bond donors",Descriptors.NumHDonors(m)),
            ("H-bond acceptors",Descriptors.NumHAcceptors(m)),
            ("Rotatable bonds",Descriptors.NumRotatableBonds(m)),
            ("Heavy atoms",m.GetNumHeavyAtoms()),
            ("Formal charge",Chem.GetFormalCharge(m)),
            ("Ring count",rdMolDescriptors.CalcNumRings(m)),
            ("Canonical SMILES",self.canonical)]
        self.props.configure(state="normal"); self.props.delete("1.0","end")
        for k,v in rows:self.props.insert("end",f"{k:<22} {v}\n")
        self.props.configure(state="disabled")

    def lookup(self):
        name=self.name_entry.get().strip()
        if not name:
            messagebox.showinfo("Compound lookup","Enter a compound name first."); return
        if requests is None:
            messagebox.showerror("Optional package missing","Install requests: pip install requests"); return
        self.status.set(f"Looking up {name} in PubChem…")
        threading.Thread(target=self._lookup_worker,args=(name,),daemon=True).start()

    def _lookup_worker(self,name):
        try:
            url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"+urllib.parse.quote(name,safe="")+"/property/IsomericSMILES,CanonicalSMILES,MolecularFormula/JSON"
            r=requests.get(url,timeout=15); r.raise_for_status()
            p=r.json()["PropertyTable"]["Properties"][0]
            smi=p.get("IsomericSMILES") or p.get("ConnectivitySMILES") or p["CanonicalSMILES"]
            self.root.after(0,lambda:self._analyze(smi,name))
        except Exception as e:
            self.root.after(0,lambda:messagebox.showerror("PubChem lookup failed",str(e)))
            self.root.after(0,lambda:self.status.set("Online lookup failed. Try another name or enter SMILES directly."))

    def copy_smiles(self):
        if not self.canonical:return
        self.root.clipboard_clear(); self.root.clipboard_append(self.canonical); self.status.set("Canonical SMILES copied.")

    def export_report(self):
        if self.current is None:
            messagebox.showinfo("No molecule","Analyze a molecule first."); return
        path=filedialog.asksaveasfilename(defaultextension=".txt",initialfile="molecule-report.txt",filetypes=[("Text report","*.txt")])
        if not path:return
        data=self.props.get("1.0","end").strip()
        with open(path,"w",encoding="utf-8") as f:
            f.write("COSMIC MOLECULE LAB REPORT\n")
            f.write(f"Name: {self.current_name}\nInput SMILES: {self.current_smiles}\nCanonical SMILES: {self.canonical}\n\n{data}\n\nComputed descriptors are estimates, not experimental measurements.\n")
        self.status.set("Report exported successfully.")

    def show_2d(self):
        if self.current is None:return
        try:
            img=Draw.MolToImage(self.current,size=(650,440),kekulize=True)
            win=tk.Toplevel(self.root); win.title("2D molecular structure"); win.configure(bg=self.bg)
            photo=ImageTk.PhotoImage(img); label=tk.Label(win,image=photo,bg=self.bg); label.image=photo; label.pack(padx=15,pady=15)
        except Exception as e:messagebox.showerror("2D drawing error",str(e))

    def reset_view(self):
        self.rot_x=-.25; self.rot_y=.35; self.zoom=1.0

    def toggle_spin(self):
        self.auto_spin=not self.auto_spin
        self.status.set("Auto spin "+("enabled." if self.auto_spin else "paused."))

    def _start_drag(self,e):self.drag=(e.x,e.y)
    def _drag(self,e):
        if self.drag:
            x,y=self.drag; self.rot_y+=(e.x-x)*.008; self.rot_x+=(e.y-y)*.008; self.drag=(e.x,e.y)
    def _wheel(self,e):self.zoom=max(.5,min(2.0,self.zoom-e.delta*.001))

    def _animate(self):
        self.viewer.delete("all")
        w=max(1,self.viewer.winfo_width()); h=max(1,self.viewer.winfo_height())
        # subtle starfield
        for i in range(65):
            x=(i*97+int(i*13.7))%w; y=(i*53+int(i*31.1))%h
            self.viewer.create_rectangle(x,y,x+2,y+2,fill="#51466e",outline="")
        if self.auto_spin and not self.drag:self.rot_y+=.012
        if self.current is not None:self._draw_molecule(w,h)
        self.root.after(35,self._animate)

    def _draw_molecule(self,w,h):
        m=Chem.AddHs(self.current)
        if m.GetNumAtoms()>160:m=Chem.RemoveHs(m)
        if AllChem.EmbedMolecule(m,randomSeed=17)==0:
            conf=m.GetConformer()
            coords=[conf.GetAtomPosition(i) for i in range(m.GetNumAtoms())]
            xs=[p.x for p in coords]; ys=[p.y for p in coords]; zs=[p.z for p in coords]
            span=max(max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs),1.0)
            scale=min(w,h)*.34/span*self.zoom
            cx=w/2; cy=h/2
            cy1=math.cos(self.rot_y); sy=math.sin(self.rot_y); cx1=math.cos(self.rot_x); sx=math.sin(self.rot_x)
            pts=[]
            for i,p in enumerate(coords):
                x=p.x; y=p.y; z=p.z
                x1=x*cy1-z*sy; z1=x*sy+z*cy1
                y1=y*cx1-z1*sx; z2=y*sx+z1*cx1
                perspective=4.8/(4.8+z2*.35)
                atom=m.GetAtomWithIdx(i); sym=atom.GetSymbol()
                pts.append((cx+x1*scale*perspective,cy+y1*scale*perspective,z2,sym,atom.GetIdx()))
            byidx={p[4]:p for p in pts}
            for b in m.GetBonds():
                a=byidx[b.GetBeginAtomIdx()]; c=byidx[b.GetEndAtomIdx()]
                self.viewer.create_line(a[0],a[1],c[0],c[1],fill="#9b8bc5",width=5)
                self.viewer.create_line(a[0],a[1],c[0],c[1],fill="#ded2ff",width=1)
            for x,y,z,sym,idx in sorted(pts,key=lambda p:p[2]):
                r={"O":15,"N":13,"C":12,"H":7}.get(sym,11)*max(.65,min(1.2,4.8/(4.8+z*.35)))
                color=COLORS.get(sym,"#ffffff")
                self.viewer.create_oval(x-r,y-r,x+r,y+r,fill=color,outline="#ffffff",width=1)
                self.viewer.create_text(x,y,text=sym,fill="#11111c",font=("Segoe UI",max(7,int(r*.8)),"bold"))

def main():
    root=tk.Tk(); CosmicLab(root); root.mainloop()

if __name__=="__main__": main()
