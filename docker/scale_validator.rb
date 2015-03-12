#!/usr/bin/ruby

# you need the gem below, a "gem install kwalify" will do the trick
require 'kwalify'
require 'yaml'

if (ARGV[0] == nil)
   puts "Error, no input scale."
   puts "Usage: ./scale_validation.rb <scale>"
   exit 1
end

# the file scale_schema.yaml should be in the same directory as this script

schema = YAML.load_file('scale_schema.yaml')

validator = Kwalify::Validator.new(schema)

document = YAML.load_file(ARGV[0])
save = YAML.load_file(ARGV[0])

errors = validator.validate(document)

$exit_status = 0

if errors && !errors.empty?
   for e in errors
       puts "[#{e.path}] #{e.message}"
   end
   $exit_status = 1
end

$project_skills = Hash.new(0)
$project_bonus = Hash.new(0)

def add_skills(skill_type, q_skills)
    q_skills.each { |skill| if (skill['percentage'] != nil) then skill_type[skill['name']] += skill['percentage'] end }
end

def questions_inspect(questions)
     position = 1
     questions.each do |question|
        question['position'] = position
	position += 1
        if (question['kind'] == "standard")
	    add_skills $project_skills, question['questions_skills']
        elsif (question['kind'] == "bonus")
            add_skills $project_bonus, question['questions_skills']
        end
     end
end

position = 1
document['sections'].each do |sec| 
    sec['position'] = position
    position += 1
    questions_inspect(sec['questions'])
end

$project_skills.each do |skill, value| 
    if value != 100
       puts "Error, total percentage for #{skill} is #{value}"
       $exit_status = 1
    end
end

$project_bonus.each do |skill, value|
    if value > 25
       puts "Error, total percentage of bonus for #{skill} is #{value}"
       $exit_status = 1
    end
end

if $exit_status == 0
   saved_scale = ARGV[0].gsub(/.ya?ml$/, '')
   saved_scale << "_save.yml"
   File.write(saved_scale, save.to_yaml)
   File.write(ARGV[0], document.to_yaml)
   puts "#{ARGV[0]} is now \e[32mvalid\e[0m ! (your initial file has been backed-up as #{saved_scale})"
else
   puts "\e[31mError\e[0m: something's wrong with your scale. Fix it, then try again."
end

exit $exit_status