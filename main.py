from jinja2 import Environment, FileSystemLoader

cv_data = {
    "summary": "Hello, this is a test."
}

env = Environment(loader=FileSystemLoader("template"))
template = env.get_template("cv_template.tex")

output = template.render(cv_data)

with open("output/cv_output.tex", "w") as f:
    f.write(output)

print("Generated output/cv_output.tex")
