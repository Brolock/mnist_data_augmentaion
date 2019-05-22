FROM debian:stable-slim as dataset

RUN apt-get update && apt-get install wget -y
RUN wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz \
         http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz \
         http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz \
         http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz


FROM python:3-slim

ARG workdir=/usr/src/data-augmentation
WORKDIR ${workdir}

VOLUME ${workdir}/data/generated_numbers

RUN pip install numpy matplotlib scipy scikit-image termcolor

RUN ln -s ${workdir}/batch_image_generator.py /usr/bin/batch_image_generator \
    && \
    ln -s ${workdir}/single_image_generator.py /usr/bin/single_image_generator

COPY --from=dataset *.gz data/
COPY . .

CMD ["single_image_generator", "--number", "1337", "--min_max", "5", "15", "--image_width", "150", "--no_display"]
