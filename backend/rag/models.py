from django.db import models
import uuid




class Paper(models.Model):
    DOMAIN_CHOICES = [
        ("CAD", "CAD"),
        ("CAM", "CAM"),
        ("CFD", "CFD"),
        ("FEA", "FEA"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512)
    authors = models.CharField(max_length=512, blank=True)
    year = models.IntegerField(null=True, blank=True)
    domain = models.CharField(max_length=10, choices=DOMAIN_CHOICES)

    file_path = models.TextField()  # local PDF path
    num_pages = models.IntegerField(null=True, blank=True)

    ingestion_status = models.CharField(
        max_length=32,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Chunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    text = models.TextField()

    page_start = models.IntegerField(null=True, blank=True)
    page_end = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=256, blank=True)

    chunk_strategy = models.CharField(max_length=64)
    chunk_index = models.IntegerField()

    embedding_model = models.CharField(max_length=128)
    vector_id = models.IntegerField(null=True, blank=True)  # FAISS index ID

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["paper", "chunk_strategy"]),
        ]

    def __str__(self):
        return f"Chunk {self.chunk_index} ({self.paper.title})"




class IngestionJob(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    paper = models.ForeignKey(
        Paper,
        on_delete=models.CASCADE,
        related_name="ingestion_jobs"
    )

    chunk_strategy = models.CharField(max_length=64)
    chunk_size = models.IntegerField()
    overlap = models.IntegerField()

    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"IngestionJob {self.id} ({self.status})"



class QueryLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    query_text = models.TextField()
    domain_filter = models.CharField(max_length=10, blank=True)

    top_k = models.IntegerField()
    retrieved_chunks = models.IntegerField()
    rerank_applied = models.BooleanField(default=False)

    latency_ms = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)





