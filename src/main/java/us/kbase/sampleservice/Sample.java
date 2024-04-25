
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


/**
 * <p>Original spec-file type: Sample</p>
 * <pre>
 * A Sample, consisting of a tree of subsamples and replicates.
 * id - the ID of the sample.
 * user - the user that saved the sample.
 * node_tree - the tree(s) of sample nodes in the sample. The the roots of all trees must
 *     be BioReplicate nodes. All the BioReplicate nodes must be at the start of the list,
 *     and all child nodes must occur after their parents in the list.
 * name - the name of the sample. Must be less than 255 characters.
 * save_date - the date the sample version was saved.
 * version - the version of the sample.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "user",
    "node_tree",
    "name",
    "save_date",
    "version"
})
public class Sample {

    @JsonProperty("id")
    private String id;
    @JsonProperty("user")
    private String user;
    @JsonProperty("node_tree")
    private List<SampleNode> nodeTree;
    @JsonProperty("name")
    private String name;
    @JsonProperty("save_date")
    private Long saveDate;
    @JsonProperty("version")
    private Long version;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public Sample withId(String id) {
        this.id = id;
        return this;
    }

    @JsonProperty("user")
    public String getUser() {
        return user;
    }

    @JsonProperty("user")
    public void setUser(String user) {
        this.user = user;
    }

    public Sample withUser(String user) {
        this.user = user;
        return this;
    }

    @JsonProperty("node_tree")
    public List<SampleNode> getNodeTree() {
        return nodeTree;
    }

    @JsonProperty("node_tree")
    public void setNodeTree(List<SampleNode> nodeTree) {
        this.nodeTree = nodeTree;
    }

    public Sample withNodeTree(List<SampleNode> nodeTree) {
        this.nodeTree = nodeTree;
        return this;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("name")
    public void setName(String name) {
        this.name = name;
    }

    public Sample withName(String name) {
        this.name = name;
        return this;
    }

    @JsonProperty("save_date")
    public Long getSaveDate() {
        return saveDate;
    }

    @JsonProperty("save_date")
    public void setSaveDate(Long saveDate) {
        this.saveDate = saveDate;
    }

    public Sample withSaveDate(Long saveDate) {
        this.saveDate = saveDate;
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

    public Sample withVersion(Long version) {
        this.version = version;
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
        return ((((((((((((((("Sample"+" [id=")+ id)+", user=")+ user)+", nodeTree=")+ nodeTree)+", name=")+ name)+", saveDate=")+ saveDate)+", version=")+ version)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
