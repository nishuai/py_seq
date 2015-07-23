import os, re
file_loc='/wrk/shni/eel/eel_parallel/align/98motif.final.simplified.align'

token='###'
chunks=[]
current_chunk=[]
i=0
for line in open(file_loc):
        if line.startswith(token) and current_chunk:
                chunks.append(current_chunk[:])
                current_chunk=[]
        current_chunk.append(line)

chunks.append(current_chunk[:])

class Alignment_stat:
        def __init__(self, alignment):
                self.coorETS=[]
                self.isSNP=[]
                self.motifs=alignment[1:-2]
                self.number=alignment[0].split()[3]
                self.sequence=alignment[-2].split()[2],alignment[-1].split()[2]
                self.ishu=self.sequence[0].startswith('ENSG')
                self.start=int(self.motifs[0].split()[2 if self.ishu else  4].split(',')[0][1:])
                self.end=int(self.motifs[-1].split()[2 if self.ishu else 4].split(',')[0][1:])
                self.length=self.end-self.start
                self.score=float(self.motifs[-1].split()[0].split('=')[1])
                self.nETS=sum(word.count('type') for word in self.motifs)
                self.seqstart=int(self.sequence[0 if self.ishu else 1].split('_')[2])
                self.chr=self.sequence[0 if self.ishu else 1].split('_')[1]
                if self.nETS!=0:
                        for i in range(len(self.motifs)):
                                if self.motifs[i].count('type'):
                                        self.coorETS.append(self.seqstart+int(self.motifs[i].split()[2 if self.ishu else 4].split(',')[0][1:]))
                                if self.motifs[i].split()[2 if self.ishu else 4].count(',')>1:
                                        self.isSNP.append(1)
