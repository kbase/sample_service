
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: DataLink</p>
 * <pre>
 * A data link from a KBase workspace object to a sample.
 *         upa - the workspace UPA of the linked object.
 *         dataid - the dataid of the linked data, if any, within the object. If omitted the
 *             entire object is linked to the sample.
 *         id - the sample id.
 *         version - the sample version.
 *         node - the sample node.
 *         createdby - the user that created the link.
 *         created - the time the link was created.
 *         expiredby - the user that expired the link, if any.
 *         expired - the time the link was expired, if at all.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "linkid",
    "upa",
    "dataid",
    "id",
    "version",
    "node",
    "createdby",
    "created",
    "expiredby",
    "expired"
})
public class DataLink {

    @JsonProperty("linkid")
    private String linkid;
    @JsonProperty("upa")
    private String upa;
    @JsonProperty("dataid")
    private String dataid;
    @JsonProperty("id")
    private String id;
    @JsonProperty("version")
    private Long version;
    @JsonProperty("node")
    private String node;
    @JsonProperty("createdby")
    private String createdby;
    @JsonProperty("created")
    private Long created;
    @JsonProperty("expiredby")
    private String expiredby;
    @JsonProperty("expired")
    private Long expired;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("linkid")
    public String getLinkid() {
        return linkid;
    }

    @JsonProperty("linkid")
    public void setLinkid(String linkid) {
        this.linkid = linkid;
    }

    public DataLink withLinkid(String linkid) {
        this.linkid = linkid;
        return this;
    }

    @JsonProperty("upa")
    public String getUpa() {
        return upa;
    }

    @JsonProperty("upa")
    public void setUpa(String upa) {
        this.upa = upa;
    }

    public DataLink withUpa(String upa) {
        this.upa = upa;
        return this;
    }

    @JsonProperty("dataid")
    public String getDataid() {
        return dataid;
    }

    @JsonProperty("dataid")
    public void setDataid(String dataid) {
        this.dataid = dataid;
    }

    public DataLink withDataid(String dataid) {
        this.dataid = dataid;
        return this;
    }

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public DataLink withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("version")
    public Long getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Long version) {
        this.version = version;
    }

    public DataLink withVersion(Long version) {
        this.version = version;
        return this;
    }

    @JsonProperty("node")
    public String getNode() {
        return node;
    }

    @JsonProperty("node")
    public void setNode(String node) {
        this.node = node;
    }

    public DataLink withNode(String node) {
        this.node = node;
        return this;
    }

    @JsonProperty("createdby")
    public String getCreatedby() {
        return createdby;
    }

    @JsonProperty("createdby")
    public void setCreatedby(String createdby) {
        this.createdby = createdby;
    }

    public DataLink withCreatedby(String createdby) {
        this.createdby = createdby;
        return this;
    }

    @JsonProperty("created")
    public Long getCreated() {
        return created;
    }

    @JsonProperty("created")
    public void setCreated(Long created) {
        this.created = created;
    }

    public DataLink withCreated(Long created) {
        this.created = created;
        return this;
    }

    @JsonProperty("expiredby")
    public String getExpiredby() {
        return expiredby;
    }

    @JsonProperty("expiredby")
    public void setExpiredby(String expiredby) {
        this.expiredby = expiredby;
    }

    public DataLink withExpiredby(String expiredby) {
        this.expiredby = expiredby;
        return this;
    }

    @JsonProperty("expired")
    public Long getExpired() {
        return expired;
    }

    @JsonProperty("expired")
    public void setExpired(Long expired) {
        this.expired = expired;
    }

    public DataLink withExpired(Long expired) {
        this.expired = expired;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((("DataLink"+" [linkid=")+ linkid)+", upa=")+ upa)+", dataid=")+ dataid)+", id=")+ id)+", version=")+ version)+", node=")+ node)+", createdby=")+ createdby)+", created=")+ created)+", expiredby=")+ expiredby)+", expired=")+ expired)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
