import io
import setuptools

with io.open("README.md", mode="r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="rutokenizer",
    version="0.0.24",
    author="Ilya Koziev",
    author_email="inkoziev@gmail.com",
    description="Russian text segmenter and tokenizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Koziev/rutokenizer",
    packages=setuptools.find_packages(),
    package_data={'rutokenizer': ['rutokenizer.dat', 'rucorpustokenizer.dat']},
    include_package_data=True,
)
