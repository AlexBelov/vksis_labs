require 'colorize'
require 'pry'
require 'yaml'
require 'logger'

logger = Logger.new('info.log')
logger.progname = 'Server'
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
    YAML::load(File.open('pipe', 'r').read)
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

  def data?
    ack && data
  end

  def confirmation?
    ack && sn && an
  end

  def fin?
    ack && fin
  end
end

previous_segment = ''
message = ""
sn, an = 1000, 0
fin_count = 0

while true
  pipe = File.open('pipe', 'r').read
  next if pipe == '' || pipe == previous_segment

  seg = TCPSegment.load
  logger.info "Receive segment".blue + " " + seg.to_s.magenta
  File.open('pipe', 'w').write('')

  if seg.step1?
    message = ""
    fin_count = 0
    sleep(1)
    an = seg.sn + 1
    step_2 = TCPSegment.new(syn:true, ack: true, sn: sn, an: an)
    logger.info "Step 2".red
    logger.info "Send segment".green + " " + step_2.to_s.magenta
    step_2.send
    previous_segment = step_2.to_yaml
  end

  if seg.data?
    if seg.sn == an - 1
      logger.info "Drop repeat".cyan
      next
    end
    sleep(1)
    an += 1 if seg.sn == an

    if rand(2) == 0
      an -= 1
    else
      message << seg.data
    end
    sn += 1
    confirmation = TCPSegment.new(ack: true, sn: sn, an: an)
    logger.info "Send confirmation segment".yellow + " " + confirmation.to_s.magenta
    confirmation.send
    previous_segment = confirmation.to_yaml
  end

  if seg.fin?
    fin_count += 1
    sleep(1)
    if fin_count == 1
      puts message
      message = ""
      sn += 1
      an += 1
      fin = TCPSegment.new(ack: true, fin: true, sn: sn, an: an)
      logger.info "Fin step 2".red
      logger.info "Send fin segment to client".green + " " + fin.to_s.magenta
      fin.send
      previous_segment = fin.to_yaml
      sn, an = 1000, 0
    end
    next
  end

  if seg.confirmation?
    if fin_count == 1
      File.open('pipe', 'w') { |file| file.write("") }
      logger.info "\n\nTHE".yellow + " END\n".blue
    end
  end
end
