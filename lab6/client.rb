require 'colorize'
require 'pry'
require 'yaml'
require 'logger'

logger = Logger.new('info.log')
logger.progname = 'Client'
logger.datetime_format = ''

class TCPSegment
  attr_accessor :syn, :ack, :fin, :sn, :an, :data

  def initialize args = nil
    return unless args
    args.each do |k,v|
      instance_variable_set("@#{k}", v) unless v.nil?
    end
  end

  def to_s
    result = ''
    result += "| SYN: #{@syn} " if @syn
    result += "| ACK: #{@ack} " if @ack
    result += "| FIN: #{@fin} " if @fin
    result += "| SN: #{@sn} " if @sn
    result += "| AN: #{@an} " if @an
    result += "| data: #{@data} " if @data
    result += '|'
    result
  end

  def send
    File.open('pipe', 'w') { |file| file.write(self.to_yaml) }
  end

  def self.load
    YAML::load(File.open('pipe', 'r').read) || TCPSegment.new
  end

  def step1?
    syn && sn == 0
  end

  def step2?
    ack && syn && sn && an
  end

  def step3?
    ack && sn == 0 && an
  end

  def confirmation?
    ack && sn && an
  end

  def fin?
    ack && fin
  end
end

while true
  line = $stdin.readline.strip
  sn, an = 0, 0

  logger.info "\n\nNEW".yellow + " SESSION\n".blue

  step_1 = TCPSegment.new(syn: true, sn: 0)
  logger.info "Step 1".red
  logger.info "Send segment".green + " " + step_1.to_s.magenta
  step_1.send
  sleep(1)

  while !(TCPSegment.load && TCPSegment.load.step2?)
  end
  seg = TCPSegment.load
  logger.info "Receive segment".blue + " " + seg.to_s.magenta
  an = seg.sn + 1
  sleep(1)

  step_3 = TCPSegment.new(ack: true, sn: 0, an: an)
  logger.info "Step 3".red
  logger.info "Send segment".green + " " + step_3.to_s.magenta
  step_3.send
  sleep(1)

  sn += 1
  logger.info "Data stream".red
  while true
    break unless line[sn-1]
    seg = TCPSegment.new(ack: true, data: line[sn-1], sn: sn, an: an)
    seg.send
    logger.info "Send segment".green + " " + seg.to_s.magenta

    sleep(1)

    while !(TCPSegment.load && TCPSegment.load.confirmation?)
    end
    seg = TCPSegment.load
    if seg.an == sn + 1
      logger.info "Receive confirmation segment".yellow + " " + seg.to_s.magenta
    else
      logger.info "I need to repeat last packet".yellow
      next
    end
    an += 1

    if rand(3) == 0
      seg = TCPSegment.new(ack: true, data: line[sn-1], sn: sn, an: an)
      seg.send
      logger.info "Send repeat".cyan + " " + seg.to_s.magenta
    end

    sn += 1
    sleep(1)
  end

  fin_step = TCPSegment.new(ack: true, fin: true, sn: sn, an: an)
  logger.info "Fin step 1".red
  logger.info "Send fin segment to server".green + " " + fin_step.to_s.magenta
  fin_step.send

  sleep(1)
  while !(TCPSegment.load && TCPSegment.load.fin?)
  end
  seg = TCPSegment.load
  logger.info "Receive fin confirmation".yellow + " " + seg.to_s.magenta

  sleep(1)
  fin_step = TCPSegment.new(ack: true, sn: sn, an: an)
  logger.info "Fin step 3".red
  logger.info "Send fin confirmation confirmation segment to server".green + " " + fin_step.to_s.magenta
  fin_step.send
end
