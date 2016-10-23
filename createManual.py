from inputModel.section import Section
from inputModel.cp2kinput import CP2Kinput
from lxml import objectify
from jinja2 import Environment, FileSystemLoader
import os
import argparse
import time

def createFile(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(path + "/" + filename, "w")
    content = ''.join(content).encode('utf-8')
    f.write(content)
    f.close()


start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('--xmlInput', '-i', '--xml', metavar='path', type=str, default="cp2k_input.xml",
                    help='Physical path to cp2k XML input file (defaults to current directory)')
parser.add_argument('--with-edit-links', '-l', action='store_true',
                    help='Adds edit buttons in manual')
args = parser.parse_args()

print("Starting CP2K manual generator")

jinja_env = Environment(loader=FileSystemLoader("templates"))
sectionTemplate = jinja_env.get_template("section.html")
mainTemplate = jinja_env.get_template("main.html")
unitsTemplate = jinja_env.get_template("units.html")
referencesTemplate = jinja_env.get_template("references.html")
genmanTemplate = jinja_env.get_template("generate_manual_howto.html")

add_edit_links = args.with_edit_links
buildDir = "build/"

CP2K_INPUT_XML = objectify.parse(args.xmlInput).getroot()
print("Loaded input XML file")

cp2k_input = CP2Kinput(
    CP2K_INPUT_XML.CP2K_VERSION.text,
    CP2K_INPUT_XML.CP2K_YEAR.text,
    CP2K_INPUT_XML.COMPILE_DATE.text,
    CP2K_INPUT_XML.COMPILE_REVISION.text,
)

print("Generating HTML pages...")
for s in CP2K_INPUT_XML.iter("SECTION"):
    section = Section(s)
    sectionHTML = sectionTemplate.render(cp2k_input=cp2k_input, section=section, add_edit_links=args.with_edit_links)
    createFile(buildDir + section.dirPath, section.fileName, sectionHTML)


mainHTML = mainTemplate.render(cp2k_input=cp2k_input)
unitsHTML = unitsTemplate.render(cp2k_input=cp2k_input)
referencesHTML = referencesTemplate.render(cp2k_input=cp2k_input)
genmanHTML = genmanTemplate.render(cp2k_input=cp2k_input)

createFile(buildDir, "index.html", mainHTML)
createFile(buildDir, "units.html", unitsHTML)
createFile(buildDir, "references.html", referencesHTML)
createFile(buildDir, "generate_manual_howto.html", genmanHTML)

print("DONE! Manual is generated in 'build' directory.")
print("Manual generated in %s seconds" % (time.time() - start_time))


