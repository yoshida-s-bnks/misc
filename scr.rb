#require './test.rb'
require 'mechanize'

agent = Mechanize.new
page = agent.get('https://bunkyosha.com/books/')


books = page.search('.title-name')

puts books.inner_text
