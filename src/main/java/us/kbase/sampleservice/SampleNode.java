
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: SampleNode</p>
 * <pre>
 * A node in a sample tree.
 * id - the ID of the node.
 * parent - the id of the parent node for the current node. BioReplicate nodes, and only
 *     BioReplicate nodes, do not have a parent.
 * type - the type of the node.
 * meta_controlled - metadata restricted by the sample controlled vocabulary and validators.
 * source_meta - the pre-transformation keys and values of the controlled metadata at the
 *     data source for controlled metadata keys. In some cases the source metadata
 *     may be transformed prior to ingestion by the Sample Service; the contents of this
 *     data structure allows for reconstructing the original representation. The metadata
 *     here is not validated other than basic size checks and is provided on an
 *     informational basis only. The metadata keys in the SourceMetadata data structure
 *     must be a subset of the meta_controlled mapping keys.
 * meta_user - unrestricted metadata.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "parent",
    "type",
    "meta_controlled",
    "source_meta",
    "meta_user"
})
public class SampleNode {

    @JsonProperty("id")
    private java.lang.String id;
    @JsonProperty("parent")
    private java.lang.String parent;
    @JsonProperty("type")
    private java.lang.String type;
    @JsonProperty("meta_controlled")
    private Map<String, Map<String, UObject>> metaControlled;
    @JsonProperty("source_meta")
    private List<SourceMetadata> sourceMeta;
    @JsonProperty("meta_user")
    private Map<String, Map<String, UObject>> metaUser;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("id")
    public java.lang.String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(java.lang.String id) {
        this.id = id;
    }

    public SampleNode withId(java.lang.String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("parent")
    public java.lang.String getParent() {
        return parent;
    }

    @JsonProperty("parent")
    public void setParent(java.lang.String parent) {
        this.parent = parent;
    }

    public SampleNode withParent(java.lang.String parent) {
        this.parent = parent;
        return this;
    }

    @JsonProperty("type")
    public java.lang.String getType() {
        return type;
    }

    @JsonProperty("type")
    public void setType(java.lang.String type) {
        this.type = type;
    }

    public SampleNode withType(java.lang.String type) {
        this.type = type;
        return this;
    }

    @JsonProperty("meta_controlled")
    public Map<String, Map<String, UObject>> getMetaControlled() {
        return metaControlled;
    }

    @JsonProperty("meta_controlled")
    public void setMetaControlled(Map<String, Map<String, UObject>> metaControlled) {
        this.metaControlled = metaControlled;
    }

    public SampleNode withMetaControlled(Map<String, Map<String, UObject>> metaControlled) {
        this.metaControlled = metaControlled;
        return this;
    }

    @JsonProperty("source_meta")
    public List<SourceMetadata> getSourceMeta() {
        return sourceMeta;
    }

    @JsonProperty("source_meta")
    public void setSourceMeta(List<SourceMetadata> sourceMeta) {
        this.sourceMeta = sourceMeta;
    }

    public SampleNode withSourceMeta(List<SourceMetadata> sourceMeta) {
        this.sourceMeta = sourceMeta;
        return this;
    }

    @JsonProperty("meta_user")
    public Map<String, Map<String, UObject>> getMetaUser() {
        return metaUser;
    }

    @JsonProperty("meta_user")
    public void setMetaUser(Map<String, Map<String, UObject>> metaUser) {
        this.metaUser = metaUser;
    }

    public SampleNode withMetaUser(Map<String, Map<String, UObject>> metaUser) {
        this.metaUser = metaUser;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((("SampleNode"+" [id=")+ id)+", parent=")+ parent)+", type=")+ type)+", metaControlled=")+ metaControlled)+", sourceMeta=")+ sourceMeta)+", metaUser=")+ metaUser)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
