from django.dispatch import Signal

document_consumption_started = Signal("filename")
document_consumption_finished = Signal("document")
document_consumer_declaration = Signal()
