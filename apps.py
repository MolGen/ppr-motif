import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.utils import to_categorical


def encode_labels(df):
    idx, labels = pd.factorize(df, sort=True)
    encoded = to_categorical(idx)
    return encoded, labels


def encode_kmers(kmers, alphabet="ACDEFGHIKLMNPQRSTVWY", k=35):
    encoded_kmers = []
    for kmer in kmers:
        kmer = kmer[:k]    # Make sure to take expected length
        try:
            idx = [alphabet.index(aa) for aa in kmer]
            encoded_kmer = to_categorical(idx, len(alphabet))
            encoded_kmer = np.array(encoded_kmer.flatten(), dtype=np.int)
            encoded_kmers.append(encoded_kmer)
        except ValueError:  # in case of non_amino_acid letters
            pass
    return np.array(encoded_kmers)


def PPR_motifs(accession, sequence, model, labels, bg="B", k=35):
    kmers = [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
    encoded_kmers = encode_kmers(kmers, k=k)
    y_probs = model.predict(encoded_kmers)
    y_classes = y_probs.argmax(axis=-1)

    starts = np.where(labels[y_classes] != bg)
    cls = y_classes[starts]
    proba = [y_probs[i][y_classes[i]] for i in starts[0]]
    motif = [sequence[s:s + k] for s in starts[0]]
    d = {"accession": accession,
         "start": starts[0],
         "end": starts[0] + k,
         "name": labels[cls],
         "score": proba,
         "strand": "+",
         "motif": motif}

    df = pd.DataFrame(d,
                      columns=['accession', 'start', 'end', 'name', 'score', 'strand', 'motif'])

    return df


def mlp_model(xshape, yshape, weights=None):
    # Define model
    model = Sequential()
    model.add(Dense(256, input_dim=xshape, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(yshape, activation='softmax'))

    if weights:
        model.load_weights(weights)

    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    return model


def read_fasta(fp):
    """https://stackoverflow.com/a/7655072"""
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name:
                yield (name, ''.join(seq))
            name, seq = line[1:], []
        else:
            seq.append(line)
    if name:
        yield (name, ''.join(seq))


labels = np.array(['B', 'E1', 'E2', 'L1', 'L2', 'P', 'P1',
                   'P2', 'S1', 'S2', 'SS'], dtype='object')

# Load Trained model
weights = "Model/Model_50k.h5"
model = mlp_model(xshape=700, yshape=11, weights=weights)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/anno', methods=['POST'])
def anno():
    raw = request.form['fasta']
    entries = pd.DataFrame()

    for accession, sequence in read_fasta(raw.splitlines()):
        entries_temp = PPR_motifs(
            accession, sequence, model, labels, bg="B", k=35)
        entries = entries.append(entries_temp, ignore_index=False)

    entries = entries.to_html(
        index=False, classes='display table table-striped table-hover" id="annotable', border=1)

    return render_template('tables.html', entries=entries)


@app.route('/curated')
def curated():
    cureated_entries = pd.read_csv(
        "datasets/ath_167_Wang_2018.bed", sep="\t", header=0)
    cureated_entries = cureated_entries.to_html(
        index=False, classes='display table table-striped table-hover" id="annotable', border=1)

    return render_template('tables.html', entries=cureated_entries)


if __name__ == '__main__':
    app.run()
